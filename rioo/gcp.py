import gspread

class GoogleSheetHandler:
    """
    A class to handle interactions with a Google Sheet, such as authentication, fetching records, and retrieving specific data.
    """

    def __init__(self, credentials: dict, sheet_id: str):
        """
        Initializes the GoogleSheetHandler instance with the necessary credentials and sheet ID.

        :param credentials: Dictionary containing the service account credentials for Google Sheets API.
        :param sheet_id: The unique ID of the Google Sheet to interact with.
        """
        self.credentials = credentials
        self.sheet_id = sheet_id
        self.gc = None
        self.worksheet = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticates with Google Sheets API using the provided service account credentials.
        """
        try:
            self.gc = gspread.service_account_from_dict(self.credentials)
            print("Successfully authenticated with Google Sheets.")
        except Exception as e:
            print(f"Authentication failed: {e}")
            raise

    def open_sheet(self, sheet_index: int = 0):
        """
        Opens the Google Sheet and selects the specified worksheet by index.

        :param sheet_index: Index of the worksheet to open (default is 0, which is the first worksheet).
        :return: The opened worksheet object.
        """
        try:
            spreadsheet = self.gc.open_by_key(self.sheet_id)
            self.worksheet = spreadsheet.get_worksheet(sheet_index)
            print(f"Opened worksheet at index {sheet_index}.")
        except Exception as e:
            print(f"Failed to open the Google Sheet: {e}")
            raise

    def get_last_n_records(self, n: int = 3):
        """
        Fetches the last 'n' records from the Google Sheet.

        :param n: Number of records to fetch from the end of the sheet (default is 3).
        :return: A list of dictionaries containing the last 'n' records.
        """
        try:
            all_records = self.worksheet.get_all_records()
            return all_records[-n:]
        except Exception as e:
            print(f"Failed to retrieve records: {e}")
            raise

# Example usage in the main script
if __name__ == "__main__":
    import config

    # Load credentials and sheet ID from the config
    credentials = config.CREDENTIALS
    sheet_id = config.GOOGLE_CHECKIN_FORM_SPREADSHEET_ID

    # Create an instance of GoogleSheetHandler
    google_sheet_handler = GoogleSheetHandler(credentials, sheet_id)

    # Authenticate and open the sheet
    google_sheet_handler.open_sheet()

    # Get the last 3 records
    try:
        last_3_records = google_sheet_handler.get_last_n_records(3)
        for record in last_3_records:
            print(record)
    except Exception as e:
        print(f"Error occurred while fetching records: {e}")


'''
{'Timestamp': '', 'Phone Number': 9123456789, 'Guest Name': 'Yash Thakre', 'Additional Guest Name': '', 'Address': 'Mumbasi', 'Guest ID Card': 'https://drive.google.com/d/bdwkidbwquakb', 'Do you Agree to the Terms and Conditions?': 'Yes', 'Signature': 'https://drive.google.com/d/bdwkidbwquakb232323', 'Check-Out Date': '09/20/2024', 'Room Number': 202, 'Payment Mode': 'UPI', 'Tariff': 1899, 'Additional Note': 'None', 'Booked By': '', 'Company': ''}
{'Timestamp': '', 'Phone Number': 1234567879, 'Guest Name': 'Hevesh Lakhwani', 'Additional Guest Name': '', 'Address': 'Nagpur', 'Guest ID Card': 'https://drive.google.com/d/bdwkidbwquakb', 'Do you Agree to the Terms and Conditions?': 'Yes', 'Signature': 'https://drive.google.com/d/bdwkidbwquakb232323', 'Check-Out Date': '09/20/2024', 'Room Number': 401, 'Payment Mode': 'CC(A)', 'Tariff': 2000, 'Additional Note': 'None', 'Booked By': '', 'Company': ''}
{'Timestamp': '', 'Phone Number': 1234567879, 'Guest Name': 'Henay', 'Additional Guest Name': '', 'Address': 'Nagpur', 'Guest ID Card': 'https://drive.google.com/d/bdwkidbwquakb', 'Do you Agree to the Terms and Conditions?': 'Yes', 'Signature': 'https://drive.google.com/d/bdwkidbwquakb232323', 'Check-Out Date': '09/20/2024', 'Room Number': 401, 'Payment Mode': 'CC(A)', 'Tariff': 2000, 'Additional Note': 'None', 'Booked By': '', 'Company': ''}
'''