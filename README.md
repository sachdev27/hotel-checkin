# Hotel Check-In System

This Google Apps Script project automates the check-in process for a hotel, integrating Google Sheets and Google Forms to manage guest information, generate pre-filled forms, and send notification emails to the reception team.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Google Apps Script Functions](#google-apps-script-functions)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Hotel Check-In System is designed to streamline the check-in process by:
- Checking if a guest exists in the database using their phone number.
- Sending check-in notification emails to the reception team.
- Adding new guests to the database or updating existing guest information.
- Generating pre-filled Google Forms for guest check-ins.
- Logging guest check-ins into Google Sheets.

## Features

- **Guest Check-In Validation:** Validates if a guest is already in the database based on their phone number.
- **Automated Emails:** Sends check-in notification emails with guest details.
- **Database Management:** Adds new guests or updates existing guest information in the database.
- **Form Prefill:** Generates pre-filled Google Forms links based on guest information.
- **Google Sheets Integration:** Logs guest check-in details into designated Google Sheets.

## Setup Instructions

1. **Clone the Repository:**
   Clone this repository to your local environment or directly copy the script files into your Google Apps Script project.

2. **Google Sheets Setup:**
   - Create a Google Sheet that will act as the guest database.
   - Create another Google Sheet for logging daily check-ins.
   - Update the script constants with the appropriate Google Sheet IDs.

3. **Google Form Setup:**
   - Create a Google Form for guest check-ins.
   - Update the script with the appropriate form field IDs to match your form.

4. **Google Drive Setup:**
   - Set up a Google Drive folder to store guest signatures.
   - Update the script with the appropriate Google Drive folder ID.

5. **Deploy as a Web App:**
   - Deploy the script as a web app if you want to create a web-based check-in interface.
   - Go to `Publish > Deploy as Web App...` in the Google Apps Script editor.

6. **Permissions:**
   - The script requires access to your Google Drive, Sheets, and Gmail to function correctly.
   - Ensure that you authorize the script when prompted.

## Google Apps Script Functions

### `checkUser(phoneNumber)`
Checks if the user exists in the guest database based on the provided phone number.

### `onFormSubmit(e)`
Handles form submissions and processes guest check-ins, including adding new guests to the database and sending emails.

### `addNewGuestToDB(phoneNumber, name, address, guestID)`
Adds or updates guest information in the database.

### `createPrefilledFormLinks(phoneNumber)`
Generates a pre-filled Google Form URL based on guest information.

### `sendCheckInEmail(name, phoneNumber)`
Sends a check-in notification email to the reception team.

### `sendSuccessfulCheckInEmail(name, phoneNumber)`
Sends a successful check-in confirmation email to the reception team.

### `getOrCreateMonthSpreadsheet(date)`
Gets or creates a Google Sheet for the current month to log check-ins.

### `getOrCreateDateSheet(spreadsheet, date)`
Gets or creates a sheet named after the day of the month for logging check-ins.

### `saveSignature(dataUrl)`
Saves a guest's signature as a PNG file in Google Drive.

## Testing

To test the functions:

1. **Run Unit Tests:**
   - Test functions are included in the script (e.g., `test_checkUser_existing`, `test_addNewGuestToDB_new_guest`).
   - Open the Google Apps Script editor and run these functions directly to validate functionality.

2. **Simulate Form Submissions:**
   - Use the `test_onFormSubmit` function to simulate form submissions and check how the system processes guest check-ins.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`feature/your-feature-name`).
3. Commit your changes.
4. Push to the branch.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
