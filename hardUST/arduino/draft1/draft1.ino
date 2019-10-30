/**
 * \par Copyright (C), 2012-2016, MakeBlock
 * @file    MeMegaPiDCMotorTest.ino
 * @author  MakeBlock
 * @version V1.0.0
 * @date    2016/05/17
 * @brief   Description: this file is sample code for MegaPi DC motor device.
 *
 * Function List:
 *    1. void MeMegaPiDCMotorTest::run(int16_t speed)
 *    2. void MeMegaPiDCMotorTest::stop(void)
 *
 * \par History:
 * <pre>
 * <Author>     <Time>        <Version>      <Descr>
 * Mark Yan     2016/05/17    1.0.0          build the new
 * </pre>
 */
#include "MeMegaPi.h"
#include "MePm25Sensor.h"
#include <SoftwareSerial.h>
#include <avr/wdt.h>

#define Access_Token GT3zq8WnHAhZphE3pCPG

#define Track1_MotorA motor1
#define Track1_Motora motor2
#define Track2_MotorA motor3
#define Track2_Motora motor4

MeWifi Wifi(PORT_5);
//MePort port(PORT_6);

MeMegaPiDCMotor motor1(PORT1A);
MeMegaPiDCMotor motor2(PORT1B);
MeMegaPiDCMotor motor3(PORT2A);
MeMegaPiDCMotor motor4(PORT2B);

Me7SegmentDisplay disp(PORT_6);
MeUltrasonicSensor ultraSensor(PORT_7); 
MeJoystick joystick(PORT_8);

MePm25Sensor myMePm25Sensor(PORT5);
int cmdTimeOutValue = 0;

uint8_t motorSpeed = 50;

typedef struct EventRegister{
  unsigned long previous_millis;
  bool check_flag;
  unsigned long duration;
};
EventRegister ThingsBoardUpload{0, false, 1000};

void setup()
{
  Serial.begin(9600);
  Wifi.begin(9600);
  myMePm25Sensor.begin(9600);
  disp.init();
  disp.set(BRIGHTNESS_2);
  delay(50);
  //Serial.println("Program Start!");
  cmdTimeOutValue = millis();
}

void loop()
{
  // Serial.print("DATA;PM1:9;PM2_5:2;PM10:3\r\n");
  unsigned long current_millis = millis();

  //=========checkFlag()======
  if(current_millis - ThingsBoardUpload.previous_millis >= ThingsBoardUpload.duration){
    //toggle LED function flag on
    ThingsBoardUpload.check_flag = true;
  }

  //===========do()===========
  if(ThingsBoardUpload.check_flag){
    thingsBoardSend();
    //reset the flag and timer
    ThingsBoardUpload.check_flag = false;
    ThingsBoardUpload.previous_millis = current_millis;
  }

  if(Serial.available()){
    String temp = Serial.readString();
    if (temp == "1"){
      disp.display(1111);
      Track1_MotorA.run(motorSpeed); /* value: between -255 and 255. */
      Track1_Motora.run(motorSpeed); /* value: between -255 and 255. */
      Track2_MotorA.run(-motorSpeed); /* value: between -255 and 255. */
      Track2_Motora.run(-motorSpeed); /* value: between -255 and 255. */
      delay(2000);
      Track1_MotorA.run(-motorSpeed); /* value: between -255 and 255. */
      Track1_Motora.run(-motorSpeed); /* value: between -255 and 255. */
      Track2_MotorA.run(+motorSpeed); /* value: between -255 and 255. */
      Track2_Motora.run(+motorSpeed); /* value: between -255 and 255. */
      delay(1800);
    }
    if (temp == "2"){
      disp.display(2222);
      Track1_MotorA.run(-motorSpeed); /* value: between -255 and 255. */
      Track1_Motora.run(-motorSpeed); /* value: between -255 and 255. */
      Track2_MotorA.run(+motorSpeed); /* value: between -255 and 255. */
      Track2_Motora.run(+motorSpeed); /* value: between -255 and 255. */
      delay(2000);
      Track1_MotorA.run(motorSpeed); /* value: between -255 and 255. */
      Track1_Motora.run(motorSpeed); /* value: between -255 and 255. */
      Track2_MotorA.run(-motorSpeed); /* value: between -255 and 255. */
      Track2_Motora.run(-motorSpeed); /* value: between -255 and 255. */
      delay(2000);
    }
  }
  


  /* read the both joystick axis values: */
  int x = joystick.readX();
  int y = joystick.readY();
  int angle = joystick.angle();
  int OffCenter = joystick.OffCenter();

  if(x > 200){
      Track1_MotorA.run(motorSpeed); /* value: between -255 and 255. */
      Track1_Motora.run(motorSpeed); /* value: between -255 and 255. */
      Track2_MotorA.run(-motorSpeed); /* value: between -255 and 255. */
      Track2_Motora.run(-motorSpeed); /* value: between -255 and 255. */
  }else if (x < -200){
      Track1_MotorA.run(-motorSpeed); /* value: between -255 and 255. */
      Track1_Motora.run(-motorSpeed); /* value: between -255 and 255. */
      Track2_MotorA.run(+motorSpeed); /* value: between -255 and 255. */
      Track2_Motora.run(+motorSpeed); /* value: between -255 and 255. */
  }else{
      Track1_MotorA.stop(); /* value: between -255 and 255. */
      Track1_Motora.stop(); /* value: between -255 and 255. */
      Track2_MotorA.stop(); /* value: between -255 and 255. */
      Track2_Motora.stop(); /* value: between -255 and 255. */
  }

}

void thingsBoardSend(){
  myMePm25Sensor.rxloop();
  uint16_t pm1_0 = myMePm25Sensor.readPm1_0Concentration();
  uint16_t pm2_5 = myMePm25Sensor.readPm2_5Concentration();
  uint16_t pm10 = myMePm25Sensor.readPm10Concentration();
  int uS = ultraSensor.distanceCm();
  //Serial.print(uS);
  // Serial.print("DATA;PM1:");  Serial.print(pm1_0); Serial.print(";");
  // Serial.print("PM2_5:");  Serial.print(pm2_5); Serial.print(";");
  // Serial.print("PM10:");  Serial.print(pm10); Serial.print(";");
  // Serial.print("UltraSonic:");  Serial.print(uS); Serial.print("\r\n");
  
  Serial.print("DATA;PM1:");  Serial.print(pm1_0); Serial.print(";");
  Serial.print("PM2_5:");  Serial.print(pm2_5); Serial.print(";");
  Serial.print("PM10:");  Serial.print(pm10); Serial.print("\r\n");
}
