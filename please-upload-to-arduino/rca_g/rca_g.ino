// Raspbot Remote Control Application (Raspbot RCA-G), Arduino Instructions for Serial Commandment
// Performs tasks as per requested through serial, also will return sensor when requested.
// Based off of Seeed Studio sensor examples (Dust and ToF). 
// Supports RFP Enceladus and Upgrade #1 sets atop the base set.

// 12 and 9 -> MotorDirection and Brake for A
// 13 and 8 -> MotorDirection and Brake for B
// 3 -> Analog motor speed input for A
// 11 -> Analog motor speed input for B
// 10 -> Grove Dust Sensor, input
// 2 -> Relay Signal for Buck Converter Toggle
// 4 -> Relay Signal for Raspberry Pi Draw Toggle (Buck Converter/Charger Station)
// 5 -> Relay Signal for Arduino Motor Shield Toggle 

int incomingData;
unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 3000;
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float concentration = 0;
char dust_serial_array[2];

#include "Seeed_vl53l0x.h"
Seeed_vl53l0x VL53L0X;

// This was from the original example sketch, it does some sort of compatability check with serial. Uncomment if needed.
//#ifdef ARDUINO_SAMD_VARIANT_COMPLIANCE
//  #define SERIAL SerialUSB
//#else
//  #define SERIAL Serial
//#endif

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(12, OUTPUT);
  pinMode(9, OUTPUT);
  
  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);

  pinMode(3, OUTPUT);
  pinMode(11, OUTPUT);
  
  pinMode(10, INPUT);

  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  
  VL53L0X_Error Status = VL53L0X_ERROR_NONE;
  Status=VL53L0X.VL53L0X_common_init();
  if(VL53L0X_ERROR_NONE!=Status)
  {
    Serial.println("start vl53l0x mesurement failed!");
    VL53L0X.print_pal_error(Status);
    while(1);
  }
  
  VL53L0X.VL53L0X_long_distance_ranging_init();
  
  if(VL53L0X_ERROR_NONE!=Status)
  {
    Serial.println("start vl53l0x mesurement failed!");
    VL53L0X.print_pal_error(Status);
    while(1);
  }
}

void loop() {
  // key
  // * = Battery Level
  
  // F, B, Arrest = Forwards, Backwards, Arrest
  // W, X = Right Forwards, Backwards
  // Y, Z = Left Forwards, Backwards
  // D = Dust Sensor (Enceladus RFP)
  // T = Distance (Enceladus RFP)

  if (Serial.available() > 0) {

    incomingData = Serial.read();

    if (incomingData == '*') {
      int value = analogRead(A0);
      float voltage = value * (5.0 / 1023.0);
      Serial.println(voltage);
      // Serial.write(voltage);
      // Serial.write('\n')
    }

    if (incomingData == '>') {
      int value = analogRead(A1);
      float voltage = value * (5.0 / 1023.0);
      Serial.println(voltage);
      // Serial.write(voltage);
      // Serial.write('\n')
    }    
    
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

    if (incomingData == 'D') {
      starttime = millis();
      duration = pulseIn(10, LOW);
      lowpulseoccupancy = lowpulseoccupancy+duration;
  
      if ((millis()-starttime) > sampletime_ms){
          ratio = lowpulseoccupancy/(sampletime_ms*10.0);  // Integer percentage 0=>100
          concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve
          dust_serial_array[0] = char(lowpulseoccupancy);
          dust_serial_array[1] = char(ratio);
          dust_serial_array[2] = char(concentration);
          Serial.write(dust_serial_array[0]);
          Serial.write('\n');
          Serial.write(dust_serial_array[1]);
          Serial.write('\n');
          Serial.write(dust_serial_array[2]);
          Serial.write('\n');
          lowpulseoccupancy = 0;
          starttime = millis();
      }
    }

    if (incomingData == 'T') {
      VL53L0X_RangingMeasurementData_t RangingMeasurementData;
      VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    
      memset(&RangingMeasurementData,0,sizeof(VL53L0X_RangingMeasurementData_t));
      Status=VL53L0X.PerformSingleRangingMeasurement(&RangingMeasurementData);
      if(VL53L0X_ERROR_NONE==Status) {
        if(RangingMeasurementData.RangeMilliMeter>=2000) {
          Serial.write("(out of range)");
          Serial.write('\n');
        }
        else {
          Serial.println(RangingMeasurementData.RangeMilliMeter);
          Serial.write('\n');
        }
      }
      else {
        Serial.write("(fail)");
        Serial.write('\n');
      }
    }
  }
}
