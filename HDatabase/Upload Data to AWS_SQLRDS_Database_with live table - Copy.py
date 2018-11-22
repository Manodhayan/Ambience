# REST API endpoint, given to you when you create an API streaming dataset
# Will be of the format: https://api.powerbi.com/beta/<tenant id>/datasets/< dataset id>/rows?key=<key id>

import ttn
from datetime import datetime
import pyodbc
connected=False
'''Connect to the Database'''
try:

    cnx=pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-4C8R5ER\HOSPSQLSERVER;'
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
    query=(("UPDATE hospital_A_live SET Timestamp=?,Room =?,Temperature=?,Humidity=? WHERE Room =?"))
    query_data=(datetime.now(),room,temperature,humidity,room)
    cursor.execute(query, query_data)
    print("Database is Updated!!!")
    cursor.close()

if connected:
    data_handler = handler.data()
    data_handler.set_uplink_callback(uplink_callback)
    data_handler.connect()

