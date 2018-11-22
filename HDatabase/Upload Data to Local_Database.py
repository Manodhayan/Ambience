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
    'lora_feather':'Neurosurgical Ward',
    'lora_feather_2':'Geriatrics Ward',
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



def Send_Alert(time,room,temperature,humidity,pressure):
    if( temperature<21 or temperature>28 or humidity>75 or humidity<40):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("manodhayan.18.2@protosem.tech","protomano98")
            MSG= "Your {} gone Critical!\nTemperature is at {}\nHumidity is at {}\n on {}".format(room,temperature,humidity,time)
            SUBJECT = "Warning!:{}".format(room)
            msg = 'Subject: {}\n\n{}'.format(SUBJECT,MSG)
            rec = ['manodhayan.18.2@protosem.tech','ems@tenxhealthtech.com','mithun.18.2@protosem.tech','sanjay.18.2@protosem.tech']
            server.sendmail("manodhayan.18.2@protosem.tech",rec, msg)
            server.quit()
            print("Alert has been sent to the user!")
        except:
            print("Error! Unable to send Alert to the User")

def uplink_callback(msg, client):
    print("Received uplink from ", msg.dev_id)
    query=(("INSERT INTO hospital_A"
               "(Timestamp, Room, Temperature, Humidity, Pressure) "
               "VALUES (?, ?, ?, ?, ?)"))
    cursor = cnx.cursor()
    room=device_list[msg.dev_id];temperature=round(msg.payload_fields.Celsius,2)
    humidity=round(msg.payload_fields.Moisture,2)
    pressure=round(msg.payload_fields.Pressure,2)/10
    
    query_data=(datetime.now(),room,temperature,humidity,pressure)
    print(query,query_data)
  
    cursor.execute(query, query_data)
    cnx.commit()
    
    #Alert User
    #Send_Alert(datetime.now(),room,temperature,humidity,pressure)

    #For live data
    query=(("UPDATE hospital_A_live SET Timestamp=?,Room =?,Temperature=?,Humidity=?,Pressure= ? WHERE Room = ?"))
    query_data=(datetime.now(),room,temperature,humidity,pressure,room)
    cursor.execute(query, query_data)
    print("Local Database is Updated!!!")
    cursor.close()

if connected:
    data_handler = handler.data()
    data_handler.set_uplink_callback(uplink_callback)
    data_handler.connect()
