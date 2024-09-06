import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation

# Load the workbook
file_path = 'Daily Report Template.xlsx'
wb = openpyxl.load_workbook(file_path, data_only=False)

# Delete sheets "Day2" to "Day31" if they exist
for day in range(2, 32):
    sheet_name = f"Day{day}"
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]

# Get the sheet "Day1" as the template
template_sheet = wb['Day1']

# Create new sheets from Day 2 to Day 31
for day in range(2, 32):
    # Copy the "Day1" sheet to a new sheet with the corresponding day number
    new_sheet_name = f'Day{day}'
    new_sheet = wb.copy_worksheet(template_sheet)
    new_sheet.title = new_sheet_name

    # Copy the data validation (dropdown lists) from the template
    for validation in template_sheet.data_validations.dataValidation:
        new_validation = DataValidation(
            type=validation.type, formula1=validation.formula1, formula2=validation.formula2,
            allow_blank=validation.allow_blank, showDropDown=validation.showDropDown,
            showErrorMessage=validation.showErrorMessage, showInputMessage=validation.showInputMessage,
            prompt=validation.prompt, error=validation.error
        )
        new_validation.ranges = validation.ranges
        new_sheet.add_data_validation(new_validation)

# Save the workbook
wb.save('Report Template.xlsx')
