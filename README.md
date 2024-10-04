# Hotel Check-In System

This project automates the hotel check-in process by integrating Google Apps Script, Google Sheets, Google Forms, and Flask to manage guest information, generate pre-filled forms, and handle notifications. It supports local management using Flask and a web interface through Google Apps Script.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Google Apps Script Functions](#google-apps-script-functions)
- [Flask Server Setup](#flask-server-setup)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## DEMO
https://github.com/user-attachments/assets/b40cf00d-f7b7-4f86-ae86-30b82da181fa



## Project Overview

The **Hotel Check-In System** is a hybrid system designed to streamline the check-in process by:
- Checking guest information from a database using phone numbers.
- Managing guest data both locally via Flask and online using Google Sheets and Forms.
- Automating notification emails to the reception team.
- Creating and logging guest records using Google Sheets.

## Features

- **Guest Check-In Validation:** Verifies if the guest is already in the database based on their phone number.
- **Automated Emails:** Sends guest check-in notifications to the reception team via email.
- **Form Prefill:** Generates pre-filled Google Forms based on guest information.
- **Database Management:** Updates or adds new guest information to the Google Sheets database.
- **Flask Integration:** Local management via Flask API for real-time updates and guest card creation.
- **Google Sheets Integration:** Logs guest check-in details into Google Sheets, providing both local and online sync options.
- **System Notifications:** Uses **Plyer** to notify the system on card creation events.

## Setup Instructions

### Google Apps Script Setup

1. **Clone the Repository:**
   Clone or copy the script files from this repository into your Google Apps Script project.

2. **Google Sheets Setup:**
   - Create a Google Sheet that will act as the guest database.
   - Create another Google Sheet to log daily check-ins.
   - Update the script constants with the appropriate Google Sheet IDs.

3. **Google Form Setup:**
   - Create a Google Form for guest check-ins.
   - Update the script with the corresponding form field IDs to match your form.

4. **Google Drive Setup:**
   - Set up a Google Drive folder to store guest signatures and update the folder ID in the script.

5. **Deploy as Web App:**
   - Go to `Publish > Deploy as Web App...` in the Google Apps Script editor to make the project accessible over the web.

6. **Set Permissions:**
   - The script requires access to Google Drive, Sheets, and Gmail APIs. Ensure you authorize these permissions when prompted.

### Flask Server Setup

1. **Install Dependencies:**
   Install the required dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration File:

- Ensure the `config.py` file contains your Google credentials and sheet IDs.
- For added security, `config.py` is encrypted and can only be decrypted by the server process.

### Start the Server:
Start the Flask server by running:

```bash
python server.py
```

## Flask Server Setup

This starts the Flask app that listens for local and external requests, integrates with Google Sheets, and manages guest card creation.

### Setting Up `ngrok` (Optional for External Access)

1. **Install `ngrok`:** Download and install `ngrok` to tunnel your local Flask server and make it accessible externally.
2. **Configure `ngrok`:** Use the provided `ngrok.py` script to automate the tunneling process and make the Flask server publicly accessible via an `ngrok` URL.

## Google Apps Script Functions

### `checkUser(phoneNumber)`
- **Purpose:** Checks if a guest exists in the database based on their phone number.

### `onFormSubmit(e)`
- **Purpose:** Handles form submissions, checks guest data, and either adds or updates guests in the database.

### `addNewGuestToDB(phoneNumber, name, address, guestID)`
- **Purpose:** Adds new guest details to the Google Sheets database or updates an existing entry.

### `createPrefilledFormLinks(phoneNumber)`
- **Purpose:** Generates a pre-filled Google Form URL using guest information.

### `sendCheckInEmail(name, phoneNumber)`
- **Purpose:** Sends a check-in notification email to the reception team.

### `sendSuccessfulCheckInEmail(name, phoneNumber)`
- **Purpose:** Sends a confirmation email to the reception team when a guest successfully checks in.

### `saveSignature(dataUrl)`
- **Purpose:** Saves the guest’s signature as a PNG file in Google Drive.

## Flask Server Setup Details

### `server.py`
- **`/register` Route:** Handles both `GET` and `POST` requests for guest card creation, returning either JSON responses or rendering an HTML page.
- **Local Request Handling:** The server can distinguish between local requests (e.g., from Google Apps Script) and external requests. Local operations such as card generation and system notifications are performed accordingly.
- **Error Handling:** Implements extensive error handling to ensure the server stays active, even in critical failure scenarios.

### `gcp.py`
- **Purpose:** Manages integration with Google Cloud APIs, such as Google Sheets and Forms, using service account credentials to interact with Google services.

### `locksdk.py`
- **Purpose:** Handles interactions with the hotel’s lock system SDK for generating and managing guest cards, giving control over the hotel’s card reader system.

## Error Handling

- **Try-Except Blocks:** Extensive error handling throughout the system ensures minimal downtime, with all exceptions logged for debugging purposes.
- **Logging:** A comprehensive logging system is in place to capture and log all errors, warnings, and system events.

## Testing

### Google Apps Script Testing
To test the Google Apps Script functionality:
1. **Run Unit Tests:** Test functions like `test_checkUser_existing` and `test_addNewGuestToDB_new_guest` are included.
2. **Simulate Form Submissions:** Use the `test_onFormSubmit` function to simulate form submissions and verify that the system processes check-ins correctly.

### Flask API Testing
To test the Flask API, you can use tools like **Postman** or **cURL** to make requests:
```bash
curl -X POST http://localhost:80/register -d "record={...}"
```

## System Notifications

The system uses **Plyer** to create notifications for certain actions, such as guest card generation. These notifications can be triggered on any local system that supports the **Plyer** library. This feature ensures that important actions, like card creation, are notified instantly to the relevant system operators.

To test system notifications, make sure that your environment is set up to display local notifications, and the **Plyer** library is installed.

## Contributing

To contribute to this project:

1. Fork the repository.
2. Create a new branch (e.g., `feature/your-feature-name`).
3. Make the necessary changes and commit your updates.
4. Open a pull request for review and integration.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
