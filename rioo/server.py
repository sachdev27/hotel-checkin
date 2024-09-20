from flask import Flask, render_template, jsonify, request, redirect, url_for
import gspread
from main import RIOO  # Assuming you have the RIOO class defined in a file named RIOO.py
import os
from gcp import GoogleSheetHandler
from datetime import datetime
import config  # Assuming config contains your credentials for Google Sheets

app = Flask(__name__)
 
# Set up the RIOO (LockSDK) interface
current_dir = os.path.dirname(os.path.realpath(__file__))
sdk_path = current_dir + "\libs\LockSDK.dll"
# rioo = RIOO(sdk_path)

# Set up Google Sheet handler
google_sheet_handler = None

def init_google_sheet_handler():
    global google_sheet_handler
    if google_sheet_handler is None:
        credentials = config.CREDENTIALS
        sheet_id = config.GOOGLE_CHECKIN_FORM_SPREADSHEET_ID
        google_sheet_handler = GoogleSheetHandler(credentials, sheet_id)
    google_sheet_handler.open_sheet()

# Endpoint to check the status of the card reader
@app.route('/status')
def status():
    try: 
        # Here, we'll simulate checking the card reader's status by reading a guest card
        # If a card reader is connected and can read a card, it returns success
        # card_details = rioo.read_guest_card()
        card_details = ''
        if card_details:
            return render_template('status.html', status="Connected and reading card")
        else:
            return render_template('status.html', status="Connected but no card detected")
    except Exception as e:
        return render_template('status.html', status=f"Error: {e}")

@app.route('/register', methods=['GET', 'POST'])
def register():
    init_google_sheet_handler()
    last_3_records = google_sheet_handler.get_last_n_records(100)

    if request.method == 'POST':
        # Get selected record from the form
        selected_record = request.form.get('record')
        # print(selected_record)
        if selected_record:
            # Parse the selected record
            selected_record = eval(selected_record)  # Be cautious with eval, make sure the input is sanitized

            # Use selected record to generate the card
            room_no = f"001.001.{selected_record['Room Number']:05d}" 
            checkin_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            checkout_time = datetime.strptime(selected_record['Check-Out Date'], "%m/%d/%Y").replace(hour=12, minute=5, second=0).strftime('%Y-%m-%d %H:%M:%S')
            print(selected_record['Guest Name'],room_no,checkin_time,checkout_time)
            # Return JSON response to update the loader and card details 

            try:
                # Generate guest card using the selected record's room number and checkout time
                # result = rioo.make_guest_card(room_no, checkin_time, checkout_time)
                return jsonify({
                    "guest_name": selected_record['Guest Name'],
                    "room_no": selected_record['Room Number'],
                    "checkin_time": checkin_time,
                    "checkout_time": checkout_time
                })
            except Exception as e:
                return 

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

