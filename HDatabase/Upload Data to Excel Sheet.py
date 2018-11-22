import ttn
from datetime import datetime
import time
import random as r

'''List of devices'''
device_list={
    'lora_feather_3': 'ICU',
    'lora_feather_4': 'Surgical Ward',
    'lora_feather_5': 'Emergency Ward',
    'lora_feature_6': 'Maternity Ward'
            }

'''ttn Object Creation'''
app_id = "hospital_ambience_monitor"
access_key = "ttn-account-v2.L5teJm-Cr8-5gQWUNZMjCcTJgXfAG-_5MmowwEgqyFY"
handler = ttn.HandlerClient(app_id, access_key)
print('TTN Object is Created')

'''GSheet Object Creation'''
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Database").sheet1 # Open Excel Sheet
print('GSheet Object is Created')


def uplink_callback(msg, client):
    print("Received uplink from ", msg.dev_id)
    #print(msg)
    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    data_count=1 # Excluding headers
    for record in sheet.get_all_records():
        data_count+=1
        
    print("{} data(s) logged yet!".format(data_count))
    print([data_count,datetime.now(),device_list[msg.dev_id],msg.payload_fields.celcius,msg.payload_fields.moisture])
    try:
        sheet.insert_row([data_count,datetime.now(),device_list[msg.dev_id],msg.payload_fields.celcius,msg.payload_fields.moisture], data_count+1)
    except:
        print("Error writing to database")
    print(list_of_hashes)

data_handler = handler.data()
data_handler.set_uplink_callback(uplink_callback)
data_handler.connect()