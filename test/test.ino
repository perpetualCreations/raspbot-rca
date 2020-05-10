// Raspbot Remote Control Application (Raspbot RCA-G), Arduino Instructions for Serial Commandment
// RAKMODULE Test Sketch, Designed for Arudino Nano

// Based off of:
/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo RAK1SERVO;
Servo RAK2SERVO;

int pos1 = 0;
int pos2 = 0;
int RAK1PIN = 10; // Set these to appropriate pins, RAK1PIN should be base servo's pin
int RAK2PIN = 9;

void setup() {
  RAK1SERVO.attach(RAK1PIN);
  RAK2SERVO.attach(RAK2PIN);
  RAK1SERVO.write(90);
  delay(15);
  RAK2SERVO.write(90); // Servo Range Default 20-170
  Serial.begin(9600);
  Serial.print(RAK2SERVO.read());
}

// Tests below, uncomment whichever you fancy.

void loop() {
  
}
/*
// Sweep Test

void loop() {
  for (pos1 = 0; pos1 <= 180; pos1 += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    RAK1SERVO.write(pos1);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos1 = 180; pos1 >= 0; pos1 -= 1) { // goes from 180 degrees to 0 degrees
    RAK1SERVO.write(pos1);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos2 = 0; pos2 <= 180; pos2 += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    RAK2SERVO.write(pos2);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos2 = 180; pos2 >= 0; pos2 -= 1) { // goes from 180 degrees to 0 degrees
    RAK2SERVO.write(pos2);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}
*/

/*
// Simultaneous Sweep Test (sort of broken, upper arm segment clips into base)

void loop() {
  for (pos1 = 0; pos1 <= 180; pos1 += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    RAK1SERVO.write(pos1);              // tell servo to go to position in variable 'pos'
    RAK2SERVO.write(pos1);
    delay(10);                       // waits 15ms for the servo to reach the position
  }
  for (pos1 = 180; pos1 >= 0; pos1 -= 1) { // goes from 180 degrees to 0 degrees
    RAK1SERVO.write(pos1);              // tell servo to go to position in variable 'pos'
    RAK2SERVO.write(pos1);
    delay(10);                       // waits 15ms for the servo to reach the position
  }
}
*/
