import ttn
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
config = {
  'user': 'ambiencesqldb',
  'password': 'Ambience^DB',
  'host': 'den1.mysql2.gear.host',
  'database': 'ambiencesqldb',
  'raise_on_warnings': True
}

connected=False
try:
#     cnx = mysql.connector.connect(user='ambiencesqldb', password='Ambience^DB',
#                               host="den1.mysql2.gear.host",
#                               database='ambiencesqldb')
    cnx=mysql.connector.connect(**config)
    connected=True
    print("Database Connected!!!")
except mysql.connector.Error as err:
    connected=False
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

#DB_NAME = 'ambiencesqldb'

#cnx.database = DB_NAME       


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
    query=(("INSERT INTO hospital_D "
               "(Timestamp, Room, Temperature, Humidity) "
               "VALUES (%s, %s, %s, %s)"))
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