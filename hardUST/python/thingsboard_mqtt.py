import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import serial

# import pyTTS
# tts = pyTTS.Create()
# tts.SetVoiceByName('MSSam')
# tts.Speak("Hello, fellow Python programmer")


MegaPi_SERIAL_PORT = "COM10"
MegaPi_Serial = serial.Serial(MegaPi_SERIAL_PORT, baudrate = 9600, timeout = 1)
# MaxiPy_SSERIAL_PORT = "COM11"
# MaxiPy_Serial = serial.Serial(MaxiPy_SSERIAL_PORT, baudrate = 115200, timeout = 1)
Orion_SERIAL_PORT = "COM12"
Orion_Serial = serial.Serial(Orion_SERIAL_PORT, baudrate = 9600, timeout = 1)

MegaPi_Serial.flushInput()
#MaxiPy_Serial.flushInput()

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'GT3zq8WnHAhZphE3pCPG'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=1

#edit the json
sensor_data = {'PM1': 2, 'PM2_5': 3, 'PM10': 4}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()
print("Program Start!")
counter = 0

try:
    while True:
        QR_Received_Flag = False
        receiveMessageQR = ""
        receiveMessageMegaPi = ""
        #print("Loop")
        if MegaPi_Serial.inWaiting() >= 1:
            receiveMessageMegaPi = MegaPi_Serial.readline() # read uart buffer untill \r\n occurs
            receiveMessageMegaPi_decode = receiveMessageMegaPi.decode()
            #PM1:1 PM2_5:2 PM10:3
            #receiveMessageMegaPi_decode = "PM1:1;PM2_5:2;PM10:3\r\n"
            if receiveMessageMegaPi_decode[0:4] == "DATA":
                rxMsgMegaPi_decode_split = receiveMessageMegaPi_decode.split(';')
                rxMsgMegaPi_decode_split1_split = rxMsgMegaPi_decode_split[1].split(':')
                rxMsgMegaPi_decode_split2_split = rxMsgMegaPi_decode_split[2].split(':')
                rxMsgMegaPi_decode_split3_split = rxMsgMegaPi_decode_split[3].split(':')
                #rxMsgMegaPi_decode_split4_split = rxMsgMegaPi_decode_split[4].split(':')
                #print(str(rxMsgMegaPi_decode_split1_split[1]))
                sensor_data['PM1'] = rxMsgMegaPi_decode_split1_split[1]
                sensor_data['PM2_5'] = rxMsgMegaPi_decode_split2_split[1]
                sensor_data['PM10'] = rxMsgMegaPi_decode_split3_split[1]
                #sensor_data['UltraSonic'] = rxMsgMegaPi_decode_split4_split[1]
                MegaPi_Serial.flushInput()
                
                ## Upload to the internet
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        if Orion_Serial.inWaiting() >= 1:
            receiveMessageDown = Orion_Serial.readline() # read uart buffer untill \r\n occurs
            receiveMessageDown_decode = receiveMessageDown.decode()
            #print(type(receiveMessageQR_decode))
            #print(receiveMessageQR_decode)
            if receiveMessageDown_decode[0:4] == "DOWN":
                print("DOWN")
                counter  = counter + 1
                print(counter)
                if counter%2 == 0:
                    MegaPi_Serial.write(b'1\0')
                if counter%2 == 1:
                    MegaPi_Serial.write(b'2\0')
                Orion_Serial.flushInput()


        # if MaxiPy_Serial.inWaiting() >= 1:
        #     receiveMessageQR = MaxiPy_Serial.readline() # read uart buffer untill \r\n occurs
        #     receiveMessageQR_decode = receiveMessageQR.decode()
        #     #print(type(receiveMessageQR_decode))
        #     #print(receiveMessageQR_decode)
        #     if receiveMessageQR_decode[0:2] == "QR":
        #         #QR:1
        #         receiveMessageQR_decode[3]
        #         QR_Received_Flag = True
        #         print("receive")
        #         if receiveMessageQR_decode[3] == "1":
        #             MegaPi_Serial.write(b'1\0')
        #             print("1")
        #         elif receiveMessageQR_decode[3] == "2":
        #             print("2")
        #             MegaPi_Serial.write(b'2\0')
                
        #         MaxiPy_Serial.flushInput()
        #>>> MegaPi_Serial.readline()
        #sensor_data = MegaPi_Serial.readline()
        #sensor_data_decode = sensor_data.decode("json")
        #temp = sensor_data.decode()



        #print(sensor_data_decode)
        #print(type(sensor_data_decode))

        # sensor_data['PM1'] = 23
        # sensor_data['flame'] = 12
        # sensor_data['gas'] = 52
        # sensor_data['humidity'] = 72
        # sensor_data['rssi'] = -34
        # Sending humidity and temperature data to ThingsBoard
        

        # next_reading += INTERVAL
        # sleep_time = next_reading-time.time()
        # if sleep_time > 0:
        #     time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
