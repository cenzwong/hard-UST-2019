/*

    This is a program of nodeMCU receing MQ2 and send back value and the rssi value back to the arduino due
    created by: Issac Lee

*/

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#ifndef STASSID
#define STASSID "SERVER DUE"
#define STAPSK  "SERVER DUE"
#endif

#define nodeMCUID "RSSI_1"

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.4.1";
const uint16_t port = 333;

ESP8266WiFiMulti WiFiMulti;

WiFiClient client;

//=====pin Define===
#define pinMQ2 A0
#define pinLED1 0
#define pinLED2 1
#define pinLED3 2
#define pinLED4 3
#define pinBTN1 5

#define SMOKE_SENSOR_THRESHOLD 7000

void setup(){
    Serial.begin(9600);
    Serial.println("Program Start, version 1");

    //configure the wifi part
    wifiSetup();

    pinMode(pinMQ2, INPUT);
    pinMode(pinLED1, OUTPUT);
    pinMode(pinLED1, OUTPUT);
    pinMode(pinLED1, OUTPUT);
    pinMode(pinLED1, OUTPUT);
    pinMode(pinLED1, INPUT);


    //delay(10000); //delay time for MQ2 to warmup
}

void loop(){
    checkSmokeSensorAlarm(analogRead(pinMQ2));
    wifiSendRSSIValue();
}

bool checkSmokeSensorAlarm(int inSmokeVal){
    if(inSmokeVal > SMOKE_SENSOR_THRESHOLD){
        //Smoke detected, alarm trigger
        return true;
    }else{
        return false;
    }
}

void wifiSetup(){
    WiFi.mode(WIFI_STA);
    WiFiMulti.addAP(ssid, password);
    Serial.print("\n\nWait for WiFi...");
    while (WiFiMulti.run() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
        //it will trap to die if not connected
    }
    Serial.println("\nWiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    delay(500);

    // connecting to server 
    Serial.print("TCP connecting to ");
    Serial.print(host);
    Serial.print(':');
    Serial.println(port); 

    while (!client.connect(host, port)) {
        Serial.println("connection failed");
        Serial.println("wait 5 sec...");
        delay(5000);
    }
}

void wifiSendRSSIValue(){
    int rssi = WiFi.RSSI();
    char deviceID[50] = nodeMCUID;
    Serial.print(millis());
    Serial.print("RSSI: ");
    Serial.println(rssi);
    sprintf(deviceID, "%s:%d", nodeMCUID ,rssi);
    client.print(deviceID);
}
