"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Made by perpetualCreations

Arduino script generation tool.

You may edit generation below, or edit scripts that already have been generated.
"""

import configparser
from random import randint
from ast import literal_eval

config = configparser.read(input("Path to hardware configuration: "))

with open("rca_upload_me_session" + str(randint(1, 9999)) + ".ino", "w") as script_export:
    script = """
    // Raspbot Remote Control Application, Arduino Instructions for Serial Commandment
    // Auto-generated instructions for Arduino.
    
    // See documentation on pinouts and additional information.
    """

    if literal_eval(config["HARDWARE"]["arm"]) is True:
        # library and variable initiation for arm servos.
        script += """
        
          // Servo Library
          #include <Servo.h>
        
          // Arm Hardware Variables
          Servo RAK1SERVO;
          Servo RAK2SERVO;
        
          int RAK1POS = 0;
          int RAK2POS = 0;
          int RAK1PIN = 10;
          int RAK2PIN = 9;
          int RAK1ANGLEDIGIT = 3;
          char RAK1ANGLEDATA[] = {'0', '1', '0'};
          int RAK2ANGLEDIGIT = 3;
          char RAK2ANGLEDATA[] = {'0', '1', '0'};
          int RAKANGLEREAD = 1;
          bool RAKSERVOREADTRIGGER = false;
        """
        pass
    pass

    script += """
    
    // Common Variables
    int incomingData;
    
    void setup() {
      Serial.begin(9600);
      
      pinMode(12, OUTPUT);
      pinMode(9, OUTPUT);
    
      pinMode(3, OUTPUT);
      pinMode(11, OUTPUT);
      
      pinMode(13, OUTPUT);
      pinMode(8, OUTPUT);
      
      pinMode(10, INPUT);
    """

    if literal_eval(config["HARDWARE"]["arm"]) is True:
        # servo initiation for arm servos.
        script += """

          RAK1SERVO.attach(RAK1PIN);
          RAK2SERVO.attach(RAK2PIN);
        """
        pass
    pass

    script += """
      Serial.begin(9600);
    }
    
    void loop() {
      // key
      // F, B = Forwards, Backwards
      // W, X = Right Forwards, Backwards
      // Y, Z = Left Forwards, Backwards
      // S = Spin Clockwise
      // C = Spin Counterclockwise
      // A = Arrest
      // V = Tells Arduino Next is Angle Digit
    
      if (Serial.available() > 0) {
    
        incomingData = Serial.read(); 
    """

    if literal_eval(config["HARDWARE"]["arm"]) is True:
        # appends?
        script += """

          if (RAK1ANGLEDIGIT == 0 && RAKANGLEREAD == 1) {
            RAK1ANGLEDIGIT = 3;
            RAK1SERVO.write(int(RAK1ANGLEDATA[0] + RAK1ANGLEDIGIT[1] + RAK1ANGLEDATA[2]));
          }
        """
        pass
    pass

    script += """
    
        if (incomingData == 'F') {
          digitalWrite(12, HIGH);
          digitalWrite(9, LOW);
          analogWrite(3, 255);
          
          digitalWrite(13, LOW);
          digitalWrite(8, LOW);
          analogWrite(11, 255);
          
          delay(1000);
        }
        
        if (incomingData == 'B') {
          digitalWrite(12, LOW);
          digitalWrite(9, LOW);
          analogWrite(3, 255);
          
          digitalWrite(13, HIGH);
          digitalWrite(8, LOW);
          analogWrite(11, 255);
          
          delay(1000);
        }
        
        if (incomingData == 'A') {
          digitalWrite(9, HIGH);
          analogWrite(3, 0);
          
          digitalWrite(8, HIGH);
          analogWrite(11, 0);  
        }
        
        if (incomingData == 'W') {
          digitalWrite(13, LOW);
          digitalWrite(8, LOW);
          analogWrite(11, 255);
          
          digitalWrite(9, HIGH);
          analogWrite(3, 0);
          
          delay(1000);
        }
        
        if (incomingData == 'X') {
          digitalWrite(13, HIGH);
          digitalWrite(8, LOW);
          analogWrite(11, 255);
          
          digitalWrite(9, HIGH);
          analogWrite(3, 0);
          
          delay(1000);
        }
        
        if (incomingData == 'Y') {
          digitalWrite(8, HIGH);
          analogWrite(11, 0);
          
          digitalWrite(12, HIGH);
          digitalWrite(9, LOW);
          analogWrite(3, 255); 
          
          delay(1000);
        }
        
        if (incomingData == 'Z') {
          digitalWrite(8, HIGH);
          analogWrite(11, 0);
          
          digitalWrite(12, LOW);
          digitalWrite(9, LOW);
          analogWrite(3, 255); 
          
          delay(1000);
        }
        
        if (incomingData == 'S') {
          digitalWrite(13, HIGH);
          digitalWrite(8, LOW);
          analogWrite(3, 255); 
          
          digitalWrite(12, HIGH);
          digitalWrite(9, LOW);
          analogWrite(3, 255);
          
          delay(1000);
        }
        
        if (incomingData == 'C') {
          digitalWrite(13, HIGH);
          digitalWrite(8, LOW);
          analogWrite(3, 255); 
          
          digitalWrite(12, LOW);
          digitalWrite(9, LOW);
          analogWrite(3, 255);
          
          delay(1000);
        }
    """
    if literal_eval(config["HARDWARE"]["charger"]) is True:
        # commands appended for charger hardware
        pass
    elif literal_eval(config["HARDWARE"]["arm"]) is True:
        # commands appended for arm hardware
        pass
    pass
    script += """
      }
    }
    """
    script_export.write(script)
pass