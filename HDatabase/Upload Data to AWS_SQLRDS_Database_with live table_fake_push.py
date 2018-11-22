from datetime import datetime
import pyodbc
import time
import random
connected=False
'''Connect to the Database'''
try:

    cnx=pyodbc.connect("Driver={SQL Server};server=hospsqlserverdatabase.czbthbfxmuzs.ap-south-1.rds.amazonaws.com,1433;database=hospsqlserverdatabase;uid=manodhayan;pwd=amazonMano98",
                      autocommit=True)
    print("Successfully connected to Database Instance :)")
    connected=True

except:
    print("Error connecting to Database :(")
        
cursor = cnx.cursor()


'''List of devices'''
device_dict={
    'lora_feather_3': 'ICU',
    'lora_feather_4': 'Surgical Ward',
    'lora_feather_5': 'Emergency Ward',
    'lora_feature_6': 'Maternity Ward'
            }
device_list=['ICU','Surgical Ward','Emergency Ward','Maternity Ward']




def fake_push(room,temperature,humidity):
    query=(("INSERT INTO hospital_A"
               "(Timestamp, Room, Temperature, Humidity) "
               "VALUES (?, ?, ?,?)"))
    cursor = cnx.cursor()
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
    index=0
    while(1):
        room=device_list[index]
        temperature=random.randint(23,25)
        humidity=random.randint(60,63)
        fake_push(room,temperature,humidity)
        time.sleep(20)
        index+=1
        if(index%4==0): index=0
        
