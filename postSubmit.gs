const TEMPLATE_SPREADSHEET_ID = "";
const PARENT_FOLDER_ID = "";

/**
 * For a given year, returns the folder for that year
 * Else creates a new folder and returns it
 */
function getOrCreateYearFolder(year) {
  // Update this to change the prefix for folder name
  var folderName = "Bookings " + year;
  var parentFolder = DriveApp.getFolderById(PARENT_FOLDER_ID);
  var folders = parentFolder.getFoldersByName(folderName);

  if (folders.hasNext()) {
    return folders.next();
  } else {
    return parentFolder.createFolder(folderName);
  }
}

/**
 * For a given data, checks if a sheet for that month already exists or not
 *
 * - If the sheet doesn't exist, it creates a sheet using the template spreadsheet and returns that
 * - If the sheet exists, it returns the spreadsheet object
 */
function getOrCreateMonthSpreadsheet(date) {
  console.log(`Searching sheet for date: `, date);
  var year = date.getFullYear().toString();
  var monthYear = Utilities.formatDate(date, Session.getScriptTimeZone(), "MMMM yyyy");
  var yearFolder = getOrCreateYearFolder(year);
  console.log("Processed Date: ", monthYear);

  // Checks the script properties to identify if a sheet already exists or not
  // Script Properties is a set of key:value pairs that store project related values
  // They can be found in 'Project Settings' section
  var spreadsheetId = PropertiesService.getScriptProperties().getProperty(monthYear);

  // If spreadsheet cannot be found in script properties, creates a new one and adds that to the script properties for future use
  if (!spreadsheetId) {
    var templateSpreadsheetId = TEMPLATE_SPREADSHEET_ID;
    var templateSpreadsheet = SpreadsheetApp.openById(templateSpreadsheetId);
    var newSpreadsheet = templateSpreadsheet.copy("Bookings - " + monthYear);

    // Adds file to the year folder
    var newFile = DriveApp.getFileById(newSpreadsheet.getId());
    yearFolder.addFile(newFile);
    // Remove file that was created in the root and just keep it in year folder
    DriveApp.getRootFolder().removeFile(newFile);

    spreadsheetId = newSpreadsheet.getId();
    PropertiesService.getScriptProperties().setProperty(monthYear, spreadsheetId);
  }

  return SpreadsheetApp.openById(spreadsheetId);
}

// NOTE: On running this test, a new sheet will be added to the script properties. So delete that if needed
function test_getOrCreateMonthSpreadsheet(){
  const date = new Date(Date.now());
  console.log(date);
  const newSheet = getOrCreateMonthSpreadsheet(date);
  console.log(newSheet.getName());
}

/**
 * For a given month's spreadsheet and a given date,
 * this function retrieves or creates a sheet named "DayX" where X is the day of the month.
 *
 * @param {Spreadsheet} spreadsheet - The monthly spreadsheet
 * @param {Date} date - The date for which to get or create a sheet
 * @returns {Sheet} The sheet for the given date
 */
function getOrCreateDateSheet(spreadsheet, date) {
  var dayOfMonth = date.getDate();
  console.log("Evaluating for: ", dayOfMonth);
  var sheetName = "Day" + dayOfMonth;
  console.log(sheetName);
  var sheet = spreadsheet.getSheetByName(sheetName);
  return sheet;
}

// Note: This test is dependant on an already created spreadSheet
function test_getOrCreateDateSheet() {
  // Variables Required for test
  const spreadsheetId = "1wtNPXSzlKipZr334f-nED9w1MfRPHryfrqEh3axaAvU";
  const spreadSheet = SpreadsheetApp.openById(spreadsheetId);
  const date = new Date(Date.now());

  // Actual test
  return getOrCreateDateSheet(spreadSheet, date);
}

/**
 * Returns the row of the sheet which is empty and should be filled next
 */
function findNextEmptyRow(sheet) {
  const startRow = 4; // Start checking from row 4 (may change based on template)
  var column = sheet.getRange('A' + startRow + ':A');
  var values = column.getValues();
  console.log(values[0], values[1]);
  var ct = 0;
  while (values[ct] && values[ct][0] !== "") {
    ct++;
  }
  return startRow + ct;
}

function populateSheet(sheet, itemResponses) {
  var nextRow = findNextEmptyRow(sheet);
  console.log(nextRow);
  var rowData = [];

  console.log("POPULATING.....")
  // Map form responses to columns
  generateRowDataFromForm(itemResponses, rowData);
  rowData[COLUMN_INDEX_POSITIONS.IN] = new Date().toISOString().slice(0, 10);
  console.log(rowData);

  sheet.getRange(nextRow, 1, 1, rowData.length).setValues([rowData]);
}

function generateRowDataFromForm(itemResponses, rowData) {
  for (var i = 0; i < itemResponses.length; i++) {
    var response = itemResponses[i];
    var responseValue = response.getResponse();
    var responseTitle = response.getItem().getTitle();
    console.log("Checking for: ", response.getItem().getTitle(), " || ", response.getResponse())
    var selectedKey;
    switch(responseTitle) {
      case FORM_QUESTION_TITLES.ROOM_NUMBER:
        rowData[COLUMN_INDEX_POSITIONS.ROOM] = responseValue;
        break;
      case FORM_QUESTION_TITLES.PAYMENT_MODE:
        selectedKey = Object.keys(DROPDOWN_COLUMN_OPTIONS.PAYMENT_MODE).find(key => DROPDOWN_COLUMN_OPTIONS.PAYMENT_MODE[key] == responseValue);
        rowData[COLUMN_INDEX_POSITIONS.PAYMENT_MODE] = DROPDOWN_COLUMN_OPTIONS.PAYMENT_MODE[selectedKey];
        break;
      case FORM_QUESTION_TITLES.GUEST_NAME:
        rowData[COLUMN_INDEX_POSITIONS.NAME] = responseValue;
        break;
      case FORM_QUESTION_TITLES.TARRIF:
        rowData[COLUMN_INDEX_POSITIONS.GROSS_RATE] = responseValue;
        break;
      case FORM_QUESTION_TITLES.CHECKOUT_DATE:
        rowData[COLUMN_INDEX_POSITIONS.OUT] = responseValue;
        break;
      case FORM_QUESTION_TITLES.ADDITIONAL_NOTE:
        rowData[COLUMN_INDEX_POSITIONS.REMARK] = responseValue;
        break;
      case FORM_QUESTION_TITLES.PHONE_NUMBER:
        rowData[COLUMN_INDEX_POSITIONS.MOBILE_NO] = responseValue;
        break;
      case FORM_QUESTION_TITLES.BOOKED_BY:
        selectedKey = Object.keys(DROPDOWN_COLUMN_OPTIONS.BOOKED_BY).find(key => DROPDOWN_COLUMN_OPTIONS.BOOKED_BY[key] == responseValue);
        console.log(selectedKey,response)
        rowData[COLUMN_INDEX_POSITIONS.BOOKED_BY] = DROPDOWN_COLUMN_OPTIONS.BOOKED_BY[selectedKey]
        break;
      case FORM_QUESTION_TITLES.COMPANY:
        selectedKey = Object.keys(DROPDOWN_COLUMN_OPTIONS.COMPANY).find(key => DROPDOWN_COLUMN_OPTIONS.COMPANY[key] == responseValue);
        rowData[COLUMN_INDEX_POSITIONS.COMPANY] = DROPDOWN_COLUMN_OPTIONS.COMPANY[selectedKey]
        break;
    }
  }
}

function test_populateSheet(){
  // Variables Required for Test
  const sheet = test_getOrCreateDateSheet();
  //TODO: Submit a form and get mockItemResponse
  const mockItemResponse = ['mock-room-number'];
  populateSheet(sheet, mockItemResponse);
}

/**
 * Mapping to store the options for columns that have dropdowns
 */
const DROPDOWN_COLUMN_OPTIONS = {
  COMPANY : {
    WALKIN: "WALKIN",
    BCOM : "BCOM",
    AGODA: "AGODA",
    GO_MMT: "GO-MMT",
    BREVISTAY: "BREVISTAY"
  },
  PAYMENT_MODE: {
    CASH: "CASH",
    UPI: "UPI",
    CC_A: "CC(A)",
    PENDING: "PENDING",
    OTA_CASH: "OTA CASH",
    NEFT_A: "NEFT(A)",
    PENDING_C: "Pending(C)"
  },
  BOOKED_BY: {
    SHIFT_1: "Shift 1",
    SHIFT_2: "Shift 2",
    SHIFT_3: "Shift 3"
  }
}

const COLUMN_INDEX_POSITIONS = {
  ROOM: 0,
  BOOKED_BY: 1,
  NAME: 2,
  MOBILE_NO: 3,
  IN: 4,
  OUT: 5,
  COMPANY: 6,
  PAYMENT_MODE: 7,
  GROSS_RATE: 8,
  REMARK: 9
}

const FORM_QUESTION_TITLES = {
  ROOM_NUMBER: "Room Number",
  GUEST_NAME: "Guest Name",
  PAYMENT_MODE: "Payment Mode",
  TARRIF: "Tariff",
  CHECKOUT_DATE: "Check-Out Date",
  ADDITIONAL_NOTE: "Additional Note",
  PHONE_NUMBER: "Phone Number",
  BOOKED_BY: "Booked By",
  COMPANY: "Company"
}

function updateSheetDate(sheet, dateString) {
  // Update the date in cell A1
  sheet.getRange("A1").setValue(dateString);

  // If you have any date-dependent formulas, update them here
  // For example:
  // sheet.getRange("B5").setFormula('=SOMEFORMULA("' + dateString + '")');
}