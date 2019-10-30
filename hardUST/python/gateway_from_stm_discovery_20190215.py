# The program is tested under Python 2.7.13 only
# Because Python 3.5.3 cannot use ser.write("SELF_STRING") to send string
# 1. Local data logging
# 2. mqtt thingsboard
# 3. uart polling

############# import for UART <BEGIN> #############
#import RPi.GPIO as GPIO
import serial
import time,sys
#import string
from random import randint
############# import for UART <END> ###############


############# import for MQTT to Thingsboard <BEGIN> ############################################
import os
#import time
#import sys
#import Adafruit_DHT as dht
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'demo.thingsboard.io'
# Demo dashboard token
ACCESS_TOKEN = 'GGltFEYrhoz5WwhUMxbC'
# New dashboard token
#ACCESS_TOKEN = 'GGltFEYrhoz5WwhUMxbC'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=1

sensor_data = {'temperature': 0, 'flame': 0, 'gas': 0, 'gasb': 0, 'humidity': 0, 'rssi': 0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()
############# import for MQTT to Thingsboard <END> ##############################################


############# import for Telepot <BEGIN> #############
import datetime
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop
############# import for Telepot <BEGIN> #############


############# Setup for UART <BEGIN> ###################################
# Define the UART serial port to mini UART port ttyS0
# RPi 3B+ ==> (1) ARM Primecell PL011 ttyAMA0 <--> embedded Bluetooth module
#             (2) CPU, BCM2837 mini UART ttyS0 <--> free to use
#             (3) USB hub, ttyACMn, n = no. <--> free to use
# old RPi ==> (1) ARM Primecell PL011 ttyAMA0 <--> free to use

#SERIAL_PORT = "/dev/ttyS0"
#ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.2)
SERIAL_PORT = "/dev/ttyACM0"
ser = serial.Serial(SERIAL_PORT, baudrate = 115200, timeout = 0.3)
############# Setup for UART <END> #####################################


############# Setup for Local Data Logging <BEGIN> ###################################
from time import strftime
# Logging data locally
def log_temp(temperature,flame,gas):
    temperature = int(temperature)
    flame = int(flame)
    gas = int(gas)
    with open("/home/pi/Desktop/IoT_data.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4}\n".format(strftime("%Y-%m-%d"), strftime("%H:%M:%S"), str(temperature),str(flame),str(gas)))
############# Setup for Local Data Logging <END> #####################################

# Record start time when this programe is executed
starttime = time.strftime("%a %b %d %Y %H:%M:%S", time.localtime())

chat_id = 0
id = 99999
temperature = '99999'
flame = '99999'
gas = '89'
gas_b = '9999'
humidity = '11'
rssivalue = '99'
index = 111
index_l = 999
index_t = 9999
index_h = 99999
index_m = 999999
index_r = 9999999
counting = 0

############# Telegram bot <BEGIN> #######################################
def action(msg):
    #global chat_id
    chat_id = msg['chat']['id']
    text = msg['text']
    print ('Received: %s' % text)
    telegram_bot.sendMessage (chat_id, message)
#telegram_bot = telepot.Bot('780588064:AAGhpNay8KI5KOUSk4jRaQqMY9BahAoUfHs')
telegram_bot = telepot.Bot('780147227:AAEDtbFxTxsUSXQ07uOQpCrgiwrn0SAw_vo')
#print (telegram_bot.getMe())
#MessageLoop(telegram_bot, action).run_as_thread()
############# Telegram bot <END> #######################################


##################################        #   #   #       ##########################################
################################## Main programme <BEGIN> ##########################################
##################################        #   #   #       ##########################################
try:
    #ser.write("\n\r\n{}\r\nmsg from RPi 3B+ TX\r\n".format(starttime))
    print("{}\r\nRPi 3B+ UART program is ready".format(starttime))
    print("LoRa module:")
    
    sensor_data['temperature'] = 23
    sensor_data['flame'] = 12
    sensor_data['gas'] = 52
    sensor_data['humidity'] = 72
    sensor_data['rssi'] = -34
    # Sending flame and temperature data to ThingsBoard
    #client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    
    while True:
        time.sleep(1.5)
        
        ser.flushInput()          # clear the input uart buffer
        datalora = ser.readline() # read uart buffer untill \r\n occurs
        if datalora == b"":
            print("## NO DATA! PLEASE CHECK! ##")
        else:
            timestamp = time.strftime("%d/%m %H:%M:%S", time.localtime())
            datalora = datalora.strip()        # remove space characters
            datalora = datalora.strip(b'\x00') # remove null byte
            datalora = datalora.decode()       # change data type, <bytes> to <string>
            #print(datalora)
            for x in range(len(datalora)):
                if datalora[x] == "I" and datalora[x+1] == "D":
                    index = x
                if datalora[x] == "L":
                    index_l = x
                if datalora[x] == "T":
                    index_t = x
                if datalora[x] == "H":
                    index_h = x
                if datalora[x] == "M":
                    index_m = x
                if datalora[x] == "N":
                    index_n = x
                if datalora[x] == "R":
                    index_r = x
            #print("ID:{} L:{} T:{} A:{} B:{}".format(index,index_l,index_t,index_h,index_m))  
            #id = datalora[index+2]
            flame = datalora[index_l+1:index_t-1]
            temperature = datalora[index_t+1:index_h-1]
            humidity = datalora[index_h+1:index_m-1]
            gas = datalora[index_m+2:index_n]
            gas_b = datalora[index_n+1:index_r]
            rssivalue = datalora[index_r+1:len(datalora)]
            #log_temp(temperature,flame,gas)  #save the data in .cvs format locally
            print("{ti} ID0{i} Temp={te:<4} flame={fl:<4} GasA={gaa:<4} GasB={gab:<4} humid={hu:<2} RSSI={r} Len{le}".format(
                                                                                    ti=timestamp,
                                                                                    i=1,
                                                                                    te=temperature,
                                                                                    fl=flame,
                                                                                    gaa=gas,
                                                                                    gab=gas_b,
                                                                                    hu=humidity,
                                                                                    r=rssivalue,
                                                                                    le=len(datalora),
                                                                                    ty=type(datalora)))
            #ser.write("RPi: OK @{}\r\n".format(timestamp))
            
            ############# MQTT to Thingsboard <BEGIN> #######################################
            #print(u"Temperature: {:g}\u00b0C, flame: {:g}%".format(temperature, flame))
            try:
                gas = 1000 - int(gas)
                humidity = 110 - int(humidity)
            except ValueError:
                pass
            sensor_data['temperature'] = temperature
            sensor_data['flame'] = flame
            sensor_data['gas'] = gas
            sensor_data['gasb']=gas_b
            sensor_data['humidity'] = humidity
            sensor_data['rssi'] = rssivalue
            # Sending flame and temperature data to ThingsBoard
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
            next_reading += INTERVAL
            sleep_time = next_reading-time.time()
            #print("Data pushed to Thingsboard Successfully!")
            if sleep_time > 0:
                time.sleep(sleep_time)
            ############# MQTT to Thingsboard <END> #########################################
            
            ############# Telegram bot <BEGIN> #######################################
            # Because the int(<str>) function cannot convert an empty string to integer,
            # it shows "invalid literal for int() with base 10" if <str> is empty
            message = "** WARNING! FIRE MAY OCCUR! **\n{}".format(timestamp)
            # Send message to telegram if flame occurs
            try:
                if int(flame) > 300:
                    message = ("** WARNING! FIRE MAY OCCUR! **\n"
                       "{ti}\n"
                       "Flame level = {fl}\r\n"
                       "Temperature = {temp} deg\r\n"
                       "Humidity = {hu}%\r\n"
                       "Gas A level = {gaa}\r\n"
                        "Gas B level = {gab}\r\n".format(ti=timestamp,fl=flame,temp=temperature,hu=humidity,gaa=gas,gab=gas_b))
                    telegram_bot.sendMessage (274406752, message)
                    #telegram_bot.sendMessage (137763952, message)
            except ValueError:
                pass
            ############# Telegram bot <END> #########################################
                
except KeyboardInterrupt:
    downtime = time.strftime("%d.%m.%Y %a %H:%M:%S", time.localtime())
    #ser.write("{} RPi DOWN\r\n".format(downtime))
    print("\r\n{} KeyboardInterrupt".format(downtime))
    


except:
    errortime = time.strftime("%d.%m.%Y %a %H:%M:%S", time.localtime())
    print("Error occurs @{}".format(errortime))
    
finally:
    ser.close()
    pass

############# MQTT to Thingsboard <BEGIN> #######################
client.loop_stop()
client.disconnect()
############# MQTT to Thingsboard <END> #########################