#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 11:37:11 2020

@author: user
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:25:34 2020

@author: jaideep
"""

import http.client
import mimetypes
import json
from datetime import datetime, date,time
def Average(lst):
    return sum(lst)/len(lst)
sensor_name = ['sensor_ec_with_switch2','sensor_ec_with_switch4']
sensors = ['9C65F9FFFE6DC9EB','9C65F9FFFE6DC9ED']
conn = http.client.HTTPSConnection("qohksjpdek.execute-api.eu-central-1.amazonaws.com")
payload = "{\"page\":\"retrieveData\",\"hardware_serial\":"
headers = {
  'Access-Control-Allow-Origin': '*',
  'Content-Type': 'application/json'
}
y=[]
for sen in sensors:
    payload_final = payload + "\"" +sen+ "\" "+"}"
    print(payload_final)
    conn.request("POST", "/test/post-json", payload_final, headers)
    res = conn.getresponse()
    data = res.read()
    x  = data
    final_data = data.decode("utf-8")
    y.append(json.loads(final_data))

time_v = [[] for i in range(len(sensors))]
EC = [[] for i in range(len(sensors))]
Moisture = [[] for i in range(len(sensors))]
Soil_temp = [[] for i in range(len(sensors))]
Air_temp = [[] for i in range(len(sensors))]
Air_hum = [[] for i in range(len(sensors))]

for ci, i in enumerate(y):
    for cj, j in enumerate(i):
        j_json = json.loads(j)
        bytes_v = j_json["hex_string"]
        date_time_v = j_json["CREATED"]
        date_time_obj = datetime.strptime(date_time_v, '%Y-%m-%d %H:%M:%S')
        if (date_time_obj.date() == date(int(2020),int(8),int(12)) and date_time_obj.time() > time(00,00,1) ):
            time_v[ci].append(
                    str(int(bytes_v[20*2:20*2+2],16)+2000) +"-"+
                    str(int(bytes_v[21*2:21*2+2],16)) + "-"+
                    str(int(bytes_v[22*2:22*2+2],16)) + ";"+
                    str(int(bytes_v[23*2:23*2+2],16))+ ":"+
                    str(int(bytes_v[24*2:24*2+2],16)) + ":"+
                    str(int(bytes_v[25*2:25*2+2],16))
                    ) 
            EC[ci].append(int(bytes_v[29*2:29*2+2],16)+int(bytes_v[30*2:30*2+2],16)*16*16+int(bytes_v[31*2:31*2+2],16)*16*16*16*16+int(bytes_v[32*2:32*2+2],16)*16*16*16*16*16*16)
            Moisture[ci].append(int(bytes_v[33*2:33*2+2],16)+int(bytes_v[34*2:34*2+2],16)*16*16+int(bytes_v[35*2:35*2+2],16)*16*16*16*16+int(bytes_v[36*2:36*2+2],16)*16*16*16*16*16*16)
            Soil_temp[ci].append(int(bytes_v[37*2:37*2+2],16)+int(bytes_v[38*2:38*2+2],16)/100)
            Air_temp[ci].append(int(bytes_v[39*2:39*2+2],16)+int(bytes_v[40*2:40*2+2],16)/100)
            Air_hum[ci].append(int(bytes_v[41*2:41*2+2],16)+int(bytes_v[42*2:42*2+2],16)/100)

import matplotlib.pyplot as plt
for i in range(0,len(sensors)):
    plt.figure()
    plt.plot(EC[i])
    plt.ylabel('EC: '+sensor_name[i])
    plt.savefig('EC: '+sensor_name[i])
    plt.show()
    
    plt.figure()
    plt.plot(Moisture[i])
    plt.ylabel('Moisture: '+sensor_name[i])
    plt.savefig('Moisture: '+sensor_name[i])
    plt.show()    

    plt.figure()
    plt.plot(Soil_temp[i])
    plt.ylabel('Soil_temp: '+sensor_name[i])
    plt.savefig('Soil_temp: '+sensor_name[i])
    plt.show()    
    
    plt.figure()
    plt.plot(Air_temp[i])
    plt.ylabel('Air_temp: '+sensor_name[i])
    plt.savefig('Air_temp: '+sensor_name[i])
    plt.show()
    
    plt.figure() 
    plt.plot(Air_hum[i])
    plt.ylabel('Air_hum: '+sensor_name[i])
    plt.savefig('Air_hum: '+sensor_name[i])
    plt.show()