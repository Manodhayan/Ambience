import ttn
from datetime import datetime
import pyodbc
import pyrebase

# Firebase Configuration
config = {
  "apiKey": "AIzaSyD5RnHoHIBb5miEq04let1ZfkDr3rowlLE",
  "authDomain": "ambience-data-622cb.firebaseio.com",
  "databaseURL": "https://hospital-ambience.firebaseio.com/",
  "storageBucket": "us-central"
}
firebase = pyrebase.initialize_app(config)
firebase_data = firebase.database()
print("Connected to Firebase Instance :)")

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
    uplink_time=msg.metadata.time
    query_data=(datetime.now(),room,temperature,humidity)
    print(query,query_data)
  
    cursor.execute(query, query_data)
    cnx.commit()
    #For live data
    firebase_data.child(room).set({"time":str(datetime.now()),"temperature": temperature, "humidity": humidity})
    print("Database is Updated!!!")
    cursor.close()

if connected:
    data_handler = handler.data()
    data_handler.set_uplink_callback(uplink_callback)
    data_handler.connect()
