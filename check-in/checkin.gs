
const USER_DATA_SHEET = '';
const CHECK_IN_GOOGLE_FORM_ID = "https://docs.google.com/forms/d/e/<__ID__>/viewform?";
const GUEST_DB_SHEET_ID = '';
const CHECK_IN_SHEET_ID = '';
const EMAIL = ''
const SIGNATURE_SHEET_PAGE_NAME = 'signature'


/**
 * Google Form Field IDs to prefill the Google Form for known users
 */
const FORM_FIELD_IDS = {
  PHONE_NUMBER: "entry.1153407724",
  PRIMARY_GUEST_NAME: "entry.2062780139",
  ADDITIONAL_GUEST_NAME: "entry.1167614848",
  GUEST_ADDRESS: "entry.2146495035",
  GUEST_DOCUMENT: "entry.862391863",
  GUEST_TERMS_AGREEMENT: "entry.1335411382",
  GUEST_EMAIL_ADDRESS: ""
};


/**
 * Checks if the user exists in the guest database.
 */
function checkUser(phoneNumber) {
  const sheet = SpreadsheetApp.openById(GUEST_DB_SHEET_ID);
  const data = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    if (data[i][0] == phoneNumber) {
      const username = data[i][1];
      sendCheckInEmail(username, phoneNumber);
      const url = createPrefilledFormLinks(phoneNumber);
      return { exists: true, formUrl: url, guestID: data[i][3] };
    }
  }

  return { exists: false, formUrl: `${CHECK_IN_GOOGLE_FORM_ID}${FORM_FIELD_IDS.PHONE_NUMBER}=${phoneNumber}` };
}


/**
 * Handles form submissions and processes guest check-ins.
 */
function onFormSubmit(e) {
  const formItems = e.response.getItemResponses();
  let phoneNumber, name, address, guestID;

  // Extract form responses
  formItems.forEach(itemResponse => {
    const questionTitle = itemResponse.getItem().getTitle();
    const response = itemResponse.getResponse();

    switch (questionTitle) {
      case "Phone Number":
        phoneNumber = response;
        break;
      case "Guest Name":
        name = response;
        break;
      case "Address":
        address = response;
        break;
      case "Guest ID Card":
        guestID = response;
        break;
    }
  });

  // Process guest check-in
  addNewGuestToDB(phoneNumber, name, address, guestID);
  sendCheckInEmail(name, phoneNumber);

  // Log form responses into sheets
  const date = new Date();
  const monthSpreadsheet = getOrCreateMonthSpreadsheet(date);
  const dateSheet = getOrCreateDateSheet(monthSpreadsheet, date);
  populateSheet(dateSheet, formItems);

  // successfull checkin
  sendSuccessfulCheckInEmail(name, phoneNumber);
}

/**
 * Adds or updates guest information in the database sheet.
 */
function addNewGuestToDB(phoneNumber, name, address, guestID) {
  const userExist = checkUser(phoneNumber);
  const guestDbSheet = SpreadsheetApp.openById(GUEST_DB_SHEET_ID).getActiveSheet();
  const signSheet = SpreadsheetApp.openById(GUEST_DB_SHEET_ID).getSheetByName(SIGNATURE_SHEET_PAGE_NAME);
  const signData = signSheet.getDataRange().getValues();
  const latestSign = signData[signData.length - 1][3];

  if (!userExist.exists) {
    guestID = `https://drive.google.com/file/d/${guestID[0]}`;
    const newRowData = [phoneNumber, name, address, guestID, latestSign, new Date()];
    guestDbSheet.appendRow(newRowData);
  } else {
    const data = guestDbSheet.getDataRange().getValues();

    if (!guestID){
      addGuestInFormSheet(phoneNumber,userExist.guestID);
    }
    guestID = guestID ? `https://drive.google.com/file/d/${guestID[0]}` : userExist.guestID;

    for (let i = 1; i < data.length; i++) {
      if (data[i][0] == phoneNumber) {
        data[i][3] = guestID;
        data[i][4] = latestSign;
        data[i][5] = new Date();
        break;
      }
    }

    guestDbSheet.getRange(1, 1, data.length, data[0].length).setValues(data);
  }

  addSignatureInFormSheet(phoneNumber, latestSign);
}

/**
 * Updates the guest's signature link in the form sheet.
 */
function addSignatureInFormSheet(phoneNumber, signatureLink) {
  // Open the Google Sheet by ID
  const sheet = SpreadsheetApp.openById(CHECK_IN_SHEET_ID).getActiveSheet();
  const data = sheet.getDataRange().getValues();

  // Find the last row matching the phone number
  const lastFoundRow = data.reverse().findIndex(row => row[1] == phoneNumber);

  if (lastFoundRow !== -1) {
    // Update the signature link in the matching row
    const rowIndex = data.length - lastFoundRow;
    sheet.getRange(rowIndex, 10).setValue(signatureLink);
  }
}


/**
 * Updates the guest's ID in the form sheet.
 */
function addGuestInFormSheet(phoneNumber, guestID) {
  // Open the Google Sheet by ID
  const sheet = SpreadsheetApp.openById(CHECK_IN_SHEET_ID).getActiveSheet();
  const data = sheet.getDataRange().getValues();

  // Find the last row matching the phone number
  const lastFoundRow = data.reverse().findIndex(row => row[1] == phoneNumber);

  if (lastFoundRow !== -1) {
    // Update the guest ID in the matching row
    const rowIndex = data.length - lastFoundRow;
    sheet.getRange(rowIndex, 8).setValue(guestID);
  }
}


/**
 * Creates a prefilled Google Form URL based on guest information.
 */
function createPrefilledFormLinks(phoneNumber) {
  const sheet = SpreadsheetApp.openById(GUEST_DB_SHEET_ID);
  const data = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    if (data[i][0] == phoneNumber) {
      const phone = encodeURIComponent(data[i][0]);
      const name = encodeURIComponent(data[i][1]);
      const address = encodeURIComponent(data[i][2]);
      const document = encodeURIComponent(data[i][3]);

      const prefilledUrl = `${CHECK_IN_GOOGLE_FORM_ID}${FORM_FIELD_IDS.PRIMARY_GUEST_NAME}=${name}&${FORM_FIELD_IDS.PHONE_NUMBER}=${phone}&${FORM_FIELD_IDS.GUEST_ADDRESS}=${address}&${FORM_FIELD_IDS.GUEST_DOCUMENT}=${document}`;
      return prefilledUrl;
    }
  }
  console.error("User with this number doesn't exist!")
}

/**
 * Sends a check-in notification email to the reception team with enhanced UI.
 */
function sendCheckInEmail(name, phoneNumber) {
  const now = new Date();
  const recipient = EMAIL; // Replace with the actual reception email
  const subject = `Visitor Check-In Notification: ${now.toLocaleString()}`;

  const htmlBody = `
    <div style="font-family: Arial, sans-serif; color: #333;">
      <h2 style="color: #02406f;">Visitor Check-In Notification</h2>
      <p>Dear Reception Team,</p>
      <p>This is to notify you that a visitor has checked in.</p>
      <table style="border-collapse: collapse; width: 70%; margin-top: 20px;">
        <tr>
          <td style="padding: 10px; border: 1px solid #ccc;"><strong>Name:</strong></td>
          <td style="padding: 10px; border: 1px solid #ccc;">${name}</td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #ccc;"><strong>Phone Number:</strong></td>
          <td style="padding: 10px; border: 1px solid #ccc;">${phoneNumber}</td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #ccc;"><strong>Check-In Time:</strong></td>
          <td style="padding: 10px; border: 1px solid #ccc;">${now.toLocaleString()}</td>
        </tr>
      </table>
      <p style="margin-top: 20px;">Thank you,<br>Automated Check-In System</p>
    </div>
  `;

  MailApp.sendEmail({
    to: recipient,
    subject: subject,
    htmlBody: htmlBody
  });
}



/**
 * Sends a successful check-in confirmation email to the reception team with enhanced UI.
 */
function sendSuccessfulCheckInEmail(name, phoneNumber) {
  const now = new Date();
  const recipient = EMAIL; // Replace with the actual reception email
  const subject = `Successful Check-In Confirmation: ${name}`;

  const htmlBody = `
    <div style="font-family: Arial, sans-serif; color: #333;">
      <h2 style="color: #0361A7;">Successful Check-In Confirmation</h2>
      <p>Dear Reception Team,</p>
      <p>We are pleased to inform you that the visitor has successfully checked in.</p>
      <table style="border-collapse: collapse; width: 70%; margin-top: 20px;">
        <tr>
          <td style="padding: 10px; border: 1px solid #ccc;"><strong>Name:</strong></td>
          <td style="padding: 10px; border: 1px solid #ccc;">${name}</td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #ccc;"><strong>Phone Number:</strong></td>
          <td style="padding: 10px; border: 1px solid #ccc;">${phoneNumber}</td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #ccc;"><strong>Check-In Time:</strong></td>
          <td style="padding: 10px; border: 1px solid #ccc;">${now.toLocaleString()}</td>
        </tr>
      </table>
      <p style="margin-top: 20px;">Thank you,<br>Automated Check-In System</p>
    </div>
  `;

  MailApp.sendEmail({
    to: recipient,
    subject: subject,
    htmlBody: htmlBody
  });
}


/**
 * Handles HTTP GET requests and serves the user registration page.
 */
function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('User Registration')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}


/**
 ______   ______     ______     ______   __     __   __     ______
/\__  _\ /\  ___\   /\  ___\   /\__  _\ /\ \   /\ "-.\ \   /\  ___\
\/_/\ \/ \ \  __\   \ \___  \  \/_/\ \/ \ \ \  \ \ \-.  \  \ \ \__ \
   \ \_\  \ \_____\  \/\_____\    \ \_\  \ \_\  \ \_\\"\_\  \ \_____\
    \/_/   \/_____/   \/_____/     \/_/   \/_/   \/_/ \/_/   \/_____/
 */






/**
 * Test Cases (to be used in Google Apps Script testing environment)
 * 1. Test checkUser function with an existing phone number.
 * 2. Test checkUser function with a non-existing phone number.
 * 3. Test addNewGuestToDB function with a new guest.
 * 4. Test addNewGuestToDB function with an existing guest.
 * 5. Test createPrefilledFormLinks function with a known phone number.
 * 6. Test sendCheckInEmail to ensure email is sent correctly.
 * 7. Test form submission flow via onFormSubmit function.
 */


// Test Add sign & Guest in Check In form
function test_addSignatureCheckinForm() {
  // Test with an existing phone number
  const phoneNumber = "9899828226"; // Replace with a known existing number in your sheet
  const signLink = "https://drive.google.com/file/d/1GzXaLDYjdQGPk62MPO4qisbEv3VxpNk7/view?usp=drivesdk";
  const result = addSignatureInFormSheet(phoneNumber,signLink);
  console.log(result);
  return result;
}

function test_addGuestIdCheckinForm() {
  // Test with an existing phone number
  const phoneNumber = "9899828226"; // Replace with a known existing number in your sheet
  const guestID = "https://drive.google.com/file/d/1GzX";
  const result = addGuestInFormSheet(phoneNumber,guestID);
  console.log(result);
  return result;
}


// 1. Test Case for checkUser Function

function test_checkUser_existing() {
  // Test with an existing phone number
  const phoneNumber = "9899828226"; // Replace with a known existing number in your sheet
  const result = checkUser(phoneNumber);
  console.log(result);
  return result;
}

function test_checkUser_non_existing() {
  // Test with a non-existing phone number
  const phoneNumber = "9999999999"; // Replace with a number that does not exist in your sheet
  const result = checkUser(phoneNumber);
  console.log(result);
  return result;
}


// 2. Test Case for addNewGuestToDB Function

function test_addNewGuestToDB_new_guest() {
  // Test adding a new guest
  const phoneNumber = "8888888888"; // Replace with a new phone number
  const name = "Test User";
  const address = "Test Address";
  const guestID = "1234567890"; // Simulated guest ID

  addNewGuestToDB(phoneNumber, name, address, guestID);
  console.log("New guest added.");
}

function test_addNewGuestToDB_existing_guest() {
  // Test updating an existing guest
  const phoneNumber = "9899828226"; // Replace with an existing phone number
  const name = "Updated User"; // Name to update
  const address = "Updated Address"; // Address to update
  const guestID = null; // Simulated guest ID to update

  addNewGuestToDB(phoneNumber, name, address, guestID);
  console.log("Existing guest updated.");
}


// 3. Test Case for createPrefilledFormLinks Function
function test_createPrefilledFormLinks() {
  // Test creating a prefilled form link
  const phoneNumber = "9899828228"; // Replace with an existing phone number in your sheet
  const prefilledUrl = createPrefilledFormLinks(phoneNumber);
  console.log(prefilledUrl);
  return prefilledUrl;
}

// 4. Test Case for sendCheckInEmail Function

function test_sendCheckInEmail() {
  // Test sending a check-in email
  const name = "Test User";
  const phoneNumber = "9899828226"; // Replace with an existing phone number
  sendCheckInEmail(name, phoneNumber);
  console.log("Email sent.");
}
function test_sendCheckInSuccessfulEmail() {
  // Test sending a check-in email
  const name = "Test User";
  const phoneNumber = "9899828226"; // Replace with an existing phone number
  sendSuccessfulCheckInEmail(name, phoneNumber);
  console.log("Email sent.");
}


// 5. Test Case for onFormSubmit Function
function test_onFormSubmit() {
  // Mock a form response
  const mockResponse = {
    getItemResponses: function() {
      return [
        {
          getItem: function() {
            return { getTitle: function() { return "Phone Number"; } };
          },
          getResponse: function() { return "8888888888"; }
        },
        {
          getItem: function() {
            return { getTitle: function() { return "Guest Name"; } };
          },
          getResponse: function() { return "Test User"; }
        },
        {
          getItem: function() {
            return { getTitle: function() { return "Address"; } };
          },
          getResponse: function() { return "Test Address"; }
        },
        {
          getItem: function() {
            return { getTitle: function() { return "Guest ID Card"; } };
          },
          getResponse: function() { return "1234567890"; }
        }
      ];
    }
  };

  // Test the form submission handling
  onFormSubmit(mockResponse);
  console.log("Form submission processed.");
}
