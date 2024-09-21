from flask import Flask, render_template, jsonify, request,abort
from main import RIOO  # Assuming you have the RIOO class defined in a file named RIOO.py
import os
from gcp import GoogleSheetHandler
from datetime import datetime
import config  # Assuming config contains your credentials for Google Sheets
import logging
from ngrok import start_ngrok
from plyer import notification
app = Flask(__name__)

# Set up the RIOO (LockSDK) interface
current_dir = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the current directory
sdk_path = os.path.join(current_dir, "libs", "LockSDK.dll")  # Use os.path.join() to ensure cross-platform compatibility

# Check if the DLL exists at the specified path
if not os.path.exists(sdk_path):
    raise FileNotFoundError(f"LockSDK.dll not found at {sdk_path}")

rioo = RIOO(sdk_path)
ROOM_FORMAT = "001.001.{room_no:05d}"
# Define a custom header and token for verification
VALID_CUSTOM_HEADER = "X-Custom-Header"
current_card_data = None

# Set up Google Sheet handler
google_sheet_handler = None

def init_google_sheet_handler():
    global google_sheet_handler
    try:
        if google_sheet_handler is None:
            credentials = config.CREDENTIALS
            sheet_id = config.GOOGLE_CHECKIN_FORM_SPREADSHEET_ID
            google_sheet_handler = GoogleSheetHandler(credentials, sheet_id)
        google_sheet_handler.open_sheet()
    except Exception as e:
        logging.error("Error connecting to google services!")

def handle_request(request):
    # Verify the custom header exists and matches the valid token
    if request.method == 'POST':
        custom_header_value = request.headers.get(VALID_CUSTOM_HEADER)
        if custom_header_value == config.VALID_TOKEN:
            # Process the request
            return
        else:
            # Unauthorized access
            abort(403)
    else:
        # Method not allowed
        abort(405)

def check_if_local_request(request):
    return False if  'ngrok' in request.host else True

def show_notification(title, message):
    """
    Function to trigger a system-wide notification.
    """
    notification.notify(
        title=title,
        message=message,
        app_name='Card Created',
        timeout=30  # Duration in seconds
    )

def set_date_and_room(selected_record):
    room_no = ROOM_FORMAT.format(room_no=selected_record['Room Number'])
    checkin_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    checkout_time = datetime.strptime(selected_record['Check-Out Date'], "%m/%d/%Y").replace(hour=12, minute=5, second=0).strftime('%Y-%m-%d %H:%M:%S')

    return room_no,checkin_time,checkout_time

def clear_and_create_guest_card(room_no,checkin_time,checkout_time):
    try:
        rioo.cancel_card()
        logging.info("Clearing Card Data")
    except Exception as e:
        logging.error("Error clearing card data! : ",e)
        return False
    try:
        rioo.make_guest_card(room_no=room_no,checkin_time=checkin_time,checkout_time=checkout_time)
        logging.info("Guest card is successfully created!")
    except Exception as e:
        logging.error("Error creating guest card! : ",e)
        return False
    logging.info("Guest Card is successfully created")
    return True

def fetch_reader_status():
    card_reader_status = {'status' : '','connection': '','error_code': None}
    try:
        encoder_status = rioo.configure_lock()
        if encoder_status == 1:
            card_reader_status['status'] = "Encoder is Connected"
            card_reader_status["connection"] = "Active"
        else:
            raise Exception
    except Exception as e:
        logging.error(e)
        encoder_status = -1
        card_reader_status['status'] = "No Encoder Detected"
        card_reader_status["connection"] = "Down"

    card_reader_status['error_code'] = encoder_status
    return card_reader_status

def fetch_card_status():
    card_status = {'status' : '','error_code': None}
    try:
        encoder_status = rioo.get_card_status()
        if encoder_status == 1 :
            card_status['status'] = "Card is placed on Encoder"
            card_status['error_code'] = 1
        else:
            raise Exception
    except Exception as e:
        card_status['status'] = "Card is not placed on Encoder!"
        card_status['error_code'] = -2
    return card_status

def fetch_card_details():
    try:
        guest_card_detail = rioo.read_guest_card()
        return guest_card_detail
    except Exception as e:
        logging.error("Error reading guesting!/No Card Detected : ",e)
        return None

def _check_error(code: int):
    """
    Checks for errors in DLL function calls and raises exceptions if necessary.

    :param code: The result code from the DLL function.
    """
    if code < 1:  # OPR_OK (1) is the only success case, others are errors
        errors = {
            -1: "No card detected",
            -2: "No encoder detected",
            -3: "Invalid card",
            -4: "Card type error",
            -5: "Reading or writing error",
            -6: "Port not open",
            -7: "End of data card",
            -8: "Invalid parameter",
            -9: "Invalid operation",
            -10: "Other error",
            -11: "Port is in use",
            -12: "Communication error",
            -20: "Customer code error",
            -29: "Unregistered error",
            -30: "No Authorization Card data",
            -31: "Room number exceeds available card subarea"
        }
        error_message = errors.get(code, f"Unknown error: {code}")
        return f"Error Code {code}: {error_message}"


# Route to get the current card reader status
@app.route('/status', methods=['GET'])
def get_status():
    card_status = fetch_reader_status()
    response_data = card_status
    return jsonify(response_data)

@app.route('/read', methods=['GET'])
def read_card():
    card_details = fetch_card_details()
    return jsonify(card_details)


@app.route('/', methods=['GET', 'POST'])
def register():
    if not check_if_local_request(request=request) : handle_request(request=request)

    global current_card_data
    init_google_sheet_handler()

    if request.method == 'POST': 
        # Get selected record from the form
        selected_record = request.form.get('record')
        # print(selected_record)
        if selected_record:
            # Parse the selected record
            selected_record = eval(selected_record)  # Be cautious with eval, make sure the input is sanitized
            room_no,checkin_time,checkout_time = set_date_and_room(selected_record=selected_record)
            # Use selected record to generate the card

            # message = f"Guest: {selected_record['Guest Name']}\nRoom: {room_no}\nCheck-in: {checkin_time}\nCheck-out: {checkout_time}"
            # show_notification("Card Created", message)
            
            print(selected_record['Guest Name'],room_no,checkin_time,checkout_time)
            # Return JSON response to update the loader and card details
            try:
                status = fetch_reader_status()
                print(status)
                error_msg = _check_error(status['error_code'])
                if error_msg:
                    return jsonify({
                        "status" : "Error",
                        "message": error_msg
                    })

            except Exception as e:
                logging.error("Error: Encoder or Card Not Detected!")
                return jsonify({
                    "status" : "Error",
                    "message": error_msg
                })

            # Fetch Card Status
            try:
                status = fetch_card_status()
                print(status)
                error_msg = _check_error(status['error_code'])
                if error_msg:
                    return jsonify({
                        "status" : "Error",
                        "message": error_msg
                    })

            except Exception as e:
                logging.error("Error: Encoder or Card Not Detected!")
                return jsonify({
                    "status" : "Error",
                    "message": error_msg
                })

            try:
                # Generate guest card using the selected record's room number and checkout time
                card_creation_status = clear_and_create_guest_card(room_no=room_no,checkin_time=checkin_time,checkout_time=checkout_time)
                if card_creation_status:
                    current_card_data =  jsonify({
                        "guest_name": selected_record['Guest Name'],
                        "room_no": selected_record['Room Number'],
                        "checkin_time": checkin_time,
                        "checkout_time": checkout_time
                    })

                    # Show a notification with the card details
                    message = f"Guest: {current_card_data['guest_name']}\nRoom: {current_card_data['room_no']}\nCheck-in: {current_card_data['checkin_time']}\nCheck-out: {current_card_data['checkout_time']}"
                    show_notification("Card Created", message)

                    return current_card_data
                else:
                    return jsonify({
                        "status" : "Error",
                        "message": "Failed creating guest card!"
                    })
            except Exception as e:
                logging.error("Error")
                return jsonify({
                    "status" : "Error",
                    "message": "Failed creating guest card!"
                })


    # Get the last 3 records from Google Sheets
    try:
        last_3_records = google_sheet_handler.get_last_n_records(5)
    except Exception as e:
        return render_template('register.html', message=f"Error fetching records: {e}", records=[])

    # Render the registration form with the last 3 records in the table and dropdown
    return render_template('register.html', records=last_3_records)

# Main function to run the Flask app
if __name__ == "__main__":
    start_ngrok()
    app.run(debug=True,port=80)
