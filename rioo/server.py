import threading
import time
from flask import Flask, render_template, jsonify, request, redirect, url_for
import gspread
from main import RIOO  # Assuming you have the RIOO class defined in a file named RIOO.py
import os
from gcp import GoogleSheetHandler
from datetime import datetime
import config  # Assuming config contains your credentials for Google Sheets
import logging
app = Flask(__name__)

# Set up the RIOO (LockSDK) interface
current_dir = os.path.dirname(os.path.realpath(__file__))
sdk_path = current_dir + "\libs\LockSDK.dll"
rioo = RIOO(sdk_path)
ROOM_FORMAT = "001.001.{room_no:05d}"

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

def set_date_and_room(selected_record):
    room_no = ROOM_FORMAT.format(room_no=selected_record['Room Number'])
    checkin_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    checkout_time = datetime.strptime(selected_record['Check-Out Date'], "%m/%d/%Y").replace(hour=12, minute=5, second=0).strftime('%Y-%m-%d %H:%M:%S')

    return room_no,checkin_time,checkout_time

def clear_and_create_guest_card(room_no,checkin_time,checkout_time):
    try:
        rioo.cancel_card()
    except Exception as e:
        logging.error("Error clearing card data! : ",e)
        return False
    try:
        rioo.make_guest_card(room_no=room_no,checkin_time=checkin_time,checkout_time=checkout_time)
    except Exception as e:
        logging.error("Error creating guest card! : ",e)
        return False
    logging.info("Guest Card is successfully created")
    return True

def fetch_reader_status():
    card_reader_status = {'status' : '','connection': ''}
    try:
        # rioo.configure_lock()
        card_reader_status['status'] = "Encoder is Connected"
        card_reader_status["connection"] = "Active"
    except Exception as e:
        e = "No Encoder Detected"
        logging.error(e)
        card_reader_status['status'] = e
        card_reader_status["connection"] = "Down"
    return card_reader_status

def fetch_card_details():
    try:
        guest_card_detail = rioo.read_guest_card()
        return guest_card_detail
    except Exception as e:
        logging.error("Error reading guesting!/No Card Detected : ",e)
        return None



# Route to get the current card reader status
@app.route('/status', methods=['GET'])
def get_status():
    card_status = fetch_reader_status()
    card_detail = fetch_card_details()

    # Merging both dictionaries using unpacking
    response_data = {**card_status, **(card_detail if card_detail else {})}
    return jsonify(response_data)

@app.route('/', methods=['GET', 'POST'])
def register():
    init_google_sheet_handler()
    # last_3_records = google_sheet_handler.get_last_n_records(100)

    if request.method == 'POST':
        # Get selected record from the form
        selected_record = request.form.get('record')
        # print(selected_record)
        if selected_record:
            # Parse the selected record
            selected_record = eval(selected_record)  # Be cautious with eval, make sure the input is sanitized
            room_no,checkin_time,checkout_time = set_date_and_room(selected_record=selected_record)
            # Use selected record to generate the card

            print(selected_record['Guest Name'],room_no,checkin_time,checkout_time)
            # Return JSON response to update the loader and card details
            try:
                # Generate guest card using the selected record's room number and checkout time
                # clear_and_create_guest_card(room_no=room_no,checkin_time=checkin_time,checkout_time=checkout_time)
                pass
            except Exception as e:
                logging.error(e)

            return jsonify({
                    "guest_name": selected_record['Guest Name'],
                    "room_no": selected_record['Room Number'],
                    "checkin_time": checkin_time,
                    "checkout_time": checkout_time
                })

    # Get the last 3 records from Google Sheets
    try:
        last_3_records = google_sheet_handler.get_last_n_records(100)
    except Exception as e:
        return render_template('register.html', message=f"Error fetching records: {e}", records=[])

    # Render the registration form with the last 3 records in the table and dropdown
    return render_template('register.html', records=last_3_records)

# Main function to run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
