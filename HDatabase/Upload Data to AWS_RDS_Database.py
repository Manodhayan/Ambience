import ttn
from datetime import datetime
import pyodbc

connected=False
try:
    cnx=pyodbc.connect("Driver={SQL Server};server=hospsqlserverdatabase.czbthbfxmuzs.ap-south-1.rds.amazonaws.com,1433;database=hospsqlserverdatabase;uid=manodhayan;pwd=amazonMano98",
                      autocommit=True)
    connected=True
    print("Database Connected!!!")
except:
        print("Error Connecting to Database...")


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
    print("Database is Updated!!!")
    cursor.close()

if connected:
    data_handler = handler.data()
    data_handler.set_uplink_callback(uplink_callback)
    data_handler.connect()