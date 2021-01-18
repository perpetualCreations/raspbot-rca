// Raspbot Remote Control Application, Arduino Instructions for Serial Commandment
// Auto-Generated

// See documentation on pinouts and additional information.

// adapted from Serial Input Basics
// char data type replaced by byte

#include <Arduino.h>

// Common Variables
int incomingData;

void setup() {
    Serial.begin(9600);
    
    // Reserved Motor Pins
    pinMode(12, OUTPUT);
    pinMode(13, OUTPUT);

    pinMode(3, OUTPUT);
    pinMode(11, OUTPUT);
    
    pinMode(9, OUTPUT);
    pinMode(8, OUTPUT);
    
    // Power Distribution System Control Pins
    pinMode(4, OUTPUT);
    pinMode(2, OUTPUT);
    
    Serial.begin(9600);
}

static float voltage_get() {
    float raw = analogRead(5);
    return ((raw * 5.0000000) / 1024.000000) / (7.50/37.50);
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
    // * = Battery Voltage
    // (, ) = Switch Ext/Int Power Relay, when HIGH, internal
    // <, > = Switch Motor Power Supply MOSFET, when LOW, ON

    if (9.00 >= voltage_get()) {
        digitalWrite(2, LOW);
        digitalWrite(4, HIGH);
    }

    if (Serial.available() > 0) {

        incomingData = Serial.read();

        if (incomingData == '*') {
            Serial.println(voltage_get());
            delay(1000);
        }
        
        if (incomingData == '(') {
            digitalWrite(2, HIGH);
        }
        
        if (incomingData == ')') {
            digitalWrite(2, LOW);
        }
        
        if (incomingData == '<') {
            digitalWrite(4, HIGH);
        }
        
        if (incomingData == '>') {
            digitalWrite(4, LOW);
        }

        if (incomingData == 'F') {
            digitalWrite(12, LOW);
            digitalWrite(9, LOW);
            analogWrite(3, 255);

            digitalWrite(13, HIGH);
            digitalWrite(8, LOW);
            analogWrite(11, 255);

            delay(1000);
        }

        if (incomingData == 'B') {
            digitalWrite(12, HIGH);
            digitalWrite(9, LOW);
            analogWrite(3, 255);

            digitalWrite(13, LOW);
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

        if (incomingData == 'Z') {
            digitalWrite(13, LOW);
            digitalWrite(8, LOW);
            analogWrite(11, 255);

            digitalWrite(9, HIGH);
            analogWrite(3, 0);

            delay(1000);
        }

        if (incomingData == 'Y') {
            digitalWrite(13, HIGH);
            digitalWrite(8, LOW);
            analogWrite(11, 255);

            digitalWrite(9, HIGH);
            analogWrite(3, 0);

            delay(1000);
        }

        if (incomingData == 'X') {
            digitalWrite(8, HIGH);
            analogWrite(11, 0);
            
            digitalWrite(12, HIGH);
            digitalWrite(9, LOW);
            analogWrite(3, 255); 
            
            delay(1000);
        }

        if (incomingData == 'W') {
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
            analogWrite(11, 255); 
            
            digitalWrite(12, HIGH);
            digitalWrite(9, LOW);
            analogWrite(3, 255);
            
            delay(1000);
        }

        if (incomingData == 'C') {
            digitalWrite(13, HIGH);
            digitalWrite(8, LOW);
            analogWrite(11, 255); 
            
            digitalWrite(12, LOW);
            digitalWrite(9, LOW);
            analogWrite(3, 255);
            
            delay(1000);
        }
    }
}
