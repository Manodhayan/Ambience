# REST API endpoint, given to you when you create an API streaming dataset
# Will be of the format: https://api.powerbi.com/beta/<tenant id>/datasets/< dataset id>/rows?key=<key id>

REST_API_URL={
    'ICU':'https://api.powerbi.com/beta/3f80d8b1-b9fa-4081-8625-ff2174620d6f/datasets/2e31426b-aeac-4428-b4a3-39ef0d92a35a/rows?key=6HHYH4F7N7N6B3tjTJzkO2me%2FFxkGRIlhP27DYh%2FmlW6DhfKg0oie65CF%2FTSGaCvVBK3gRl1Ko2wnpyXhGDf%2Fw%3D%3D',
    'Surgical Ward':'https://api.powerbi.com/beta/3f80d8b1-b9fa-4081-8625-ff2174620d6f/datasets/1f9c6b51-6ea5-4f19-8123-3c0fee6896ce/rows?key=FAB%2By6eK0F5G5GsmA0rJUgfupWNmBWXLnzzh0r91SMNrB6ORzVoUq5oezWRKrVa52HRyoQzKEgNqANR%2FbYzP3Q%3D%3D',
    'Emergency Ward':'https://api.powerbi.com/beta/3f80d8b1-b9fa-4081-8625-ff2174620d6f/datasets/81b4baa3-2472-46e8-bc1a-bc1199020ace/rows?key=6dVQRN4Z5tMhsy9cEffU7n9rhA6vy7cKFry2biSJSJ9XNPqtdKSFm1gT2WaUEZ98lgz%2FQkYla0%2F2aks22ZH1ng%3D%3D',
    'Maternity Ward':'https://api.powerbi.com/beta/3f80d8b1-b9fa-4081-8625-ff2174620d6f/datasets/b016e1be-4013-4fc7-970a-e2f462ea977b/rows?key=iWTn1aSIFrx1LUzLkCv1IDszkAteZIF5oMiV3YpGJam5RwsgvavAOeM0zrkcFrT3UrYcIETg8ZCzscF0AT7pfA%3D%3D'
            }

import pandas as pd
import requests

 # set the header record
HEADER = ["Timestamp", "Humidity", "Temperature", "Room"]

import ttn
from datetime import datetime
import pyodbc
connected=False
'''Connect to the Database'''
try:

    cnx=pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-4C8R5ER;'
                       'Database=hospsqlserverdatabase;'
                      'Trusted_Connection=yes;')
    print("Successfully connected to Database Instance :)")
    connected=True

except:
    print("Error connecting to Database :(")
        
cursor = cnx.cursor()


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




def uplink_callback(msg, client):
    #print("Received uplink from ", msg.dev_id)
    query=(("INSERT INTO hospital_A"
               "(Timestamp, Room, Temperature, Humidity) "
               "VALUES (?, ?, ?,?)"))
    cursor = cnx.cursor()
    room=device_list[msg.dev_id];temperature=msg.payload_fields.celcius
    humidity=msg.payload_fields.moisture
    
    query_data=(datetime.now(),room,temperature,humidity)
    print(query,query_data)
  
    cursor.execute(query, query_data)
    cnx.commit()
    #For live data
    data_raw = []
    data_raw.append([datetime.now(),humidity,temperature,room])
    data_df = pd.DataFrame(data_raw, columns=HEADER)
    data_json = bytes(data_df.to_json(orient='records'), encoding='utf-8')
    requests.post(REST_API_URL[room], data_json)
    print("Database is Updated!!!")
    cursor.close()

if connected:
    data_handler = handler.data()
    data_handler.set_uplink_callback(uplink_callback)
    data_handler.connect()
