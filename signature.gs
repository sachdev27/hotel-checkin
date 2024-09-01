
const GOOGLE_SHEET_ID = '';
const SIGNATURE_FOLDER_ID = '';
const SIGNATURE_SHEET_PAGE_NAME = 'signature'

function doGet() {
  return HtmlService.createHtmlOutputFromFile('SignatureForm');
}

function saveSignature(dataUrl) {
  // Folder ID where the signature will be saved
  const folder = DriveApp.getFolderById(SIGNATURE_FOLDER_ID); // Replace with your Google Drive folder ID

  // Get the current date and time
  const now = new Date();
  const timestamp = Utilities.formatDate(now, Session.getScriptTimeZone(), 'yyyyMMdd_HHmmss');

  // Create a file name with the current date and time
  const fileName = 'signature_' + timestamp + '.png';

  // Create the file in the specified folder
  const blob = Utilities.newBlob('', 'image/png', fileName);
  const file = folder.createFile(blob.setBytes(Utilities.base64Decode(dataUrl.split(',')[1])));

  // Get the file URL
  const fileUrl = file.getUrl();
  const fileId = file.getId();

  // Save the file URL or ID to Google Sheets
  saveSignatureToSheet(timestamp, fileName, fileId, fileUrl);

  return fileUrl;
}

function saveSignatureToSheet(timestamp, fileName, fileId, fileUrl) {
  const sheet = SpreadsheetApp.openById(GOOGLE_SHEET_ID).getSheetByName(SIGNATURE_SHEET_PAGE_NAME);
  
  // Append the data to the sheet
  sheet.appendRow([timestamp, fileName, fileId, fileUrl]);
}
