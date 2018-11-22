import ttn
from datetime import datetime
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

connected=True


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
    temperature=msg.payload_fields.celcius
    humidity=msg.payload_fields.moisture
    #For live data
    for hall in device_list:
        if device_list[hall]=='ICU':
            temperature-=1
            humidity-=1
        elif device_list[hall]=='Emergency Ward':
            temperature+=1
            humidity+=1
        elif device_list[hall]=='Surgical Ward':
            temperature-=1
            humidity+=2

        print(device_list[hall])
        room=device_list[hall]
        firebase_data.child(room).set({"time":str(datetime.now()),"temperature": temperature, "humidity": humidity})
        print("Database is Updated!!!")
if connected:
    data_handler = handler.data()
    data_handler.set_uplink_callback(uplink_callback)
    data_handler.connect()