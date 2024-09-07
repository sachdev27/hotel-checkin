import gspread
import config

# Load credentials and sheet ID from the config
credentials = config.CREDENTIALS  
sheet_id = config.GOOGLE_CHECKIN_FORM_SPREADSHEET_ID

# Authenticate using the service account credentials
gc = gspread.service_account_from_dict(credentials)

# Open the Google Sheet by key
sh = gc.open_by_key(sheet_id)

# Select the first worksheet (adjust if necessary)
worksheet = sh.sheet1

# Fetch all records from the sheet
all_records = worksheet.get_all_records()

# Get the last 3 records (if there are less than 3, it will return all available)
last_3_records = all_records[-3:]

# Print the last 3 records
for record in last_3_records:
    print(record)

'''
{'Timestamp': '', 'Phone Number': 9123456789, 'Guest Name': 'Yash Thakre', 'Additional Guest Name': '', 'Address': 'Mumbasi', 'Guest ID Card': 'https://drive.google.com/d/bdwkidbwquakb', 'Do you Agree to the Terms and Conditions?': 'Yes', 'Signature': 'https://drive.google.com/d/bdwkidbwquakb232323', 'Check-Out Date': '09/20/2024', 'Room Number': 202, 'Payment Mode': 'UPI', 'Tariff': 1899, 'Additional Note': 'None', 'Booked By': '', 'Company': ''}
{'Timestamp': '', 'Phone Number': 1234567879, 'Guest Name': 'Hevesh Lakhwani', 'Additional Guest Name': '', 'Address': 'Nagpur', 'Guest ID Card': 'https://drive.google.com/d/bdwkidbwquakb', 'Do you Agree to the Terms and Conditions?': 'Yes', 'Signature': 'https://drive.google.com/d/bdwkidbwquakb232323', 'Check-Out Date': '09/20/2024', 'Room Number': 401, 'Payment Mode': 'CC(A)', 'Tariff': 2000, 'Additional Note': 'None', 'Booked By': '', 'Company': ''}
{'Timestamp': '', 'Phone Number': 1234567879, 'Guest Name': 'Henay', 'Additional Guest Name': '', 'Address': 'Nagpur', 'Guest ID Card': 'https://drive.google.com/d/bdwkidbwquakb', 'Do you Agree to the Terms and Conditions?': 'Yes', 'Signature': 'https://drive.google.com/d/bdwkidbwquakb232323', 'Check-Out Date': '09/20/2024', 'Room Number': 401, 'Payment Mode': 'CC(A)', 'Tariff': 2000, 'Additional Note': 'None', 'Booked By': '', 'Company': ''}
'''