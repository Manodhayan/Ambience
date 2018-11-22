import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
print(creds)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Database").sheet1
def upload_data():
    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    data_count=1 # Excluding headers
    for record in sheet.get_all_records():
        data_count+=1
    print(data_count)
    sheet.insert_row(["ICU",23,61], data_count+1)
    print(list_of_hashes)
    time.sleep(1)
    upload_data()

upload_data()