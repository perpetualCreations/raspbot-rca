"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Made by perpetualCreations

Arduino script generation tool.

You may edit generation below, or edit scripts that already have been generated.
"""

import configparser
from random import randint
from ast import literal_eval

config = configparser.ConfigParser()
config.read(input("Path to hardware configuration: "))

with open("rca_upload_me_" + str(randint(1, 9999)) + ".cpp", "w") as script_export:
    script = """// Raspbot Remote Control Application, Arduino Instructions for Serial Commandment
// Auto-Generated

// See documentation on pinouts and additional information.
"""

    if input("Using the stock Arduino IDE to upload? [y/n]: ").lower() is "n":
        script += """
#include <Arduino.h>
"""

    if literal_eval(config["HARDWARE"]["distance"]):
        script += """
#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;
"""

    script += """
// Variable Declaration
int incomingData;
int accumulatorIndex = 0;
char accumulator[64]; 
int initialMotorSpeed = 200; // must be 0-255

static float voltage_get() {
    float raw = analogRead(3);
    return ((raw * 5.0000000) / 1024.000000) / (7.50/37.50);
}
"""

    script += """
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
    
    if (voltage_get() > 9.50) {
        // if battery voltage over 9.5, close motor power supply MOSFET and switch power relay to internal
        digitalWrite(2, HIGH);
        digitalWrite(4, LOW);
    }
    else {
        digitalWrite(2, LOW);
        digitalWrite(4, HIGH);
    }
    """

    if literal_eval(config["HARDWARE"]["distance"]):
        script += """
    // XSHUT of VL53L0X ToF Sensor    
    pinMode(7, OUTPUT);
    
    // TOF INIT
    sensor.setTimeout(500);
    sensor.init();
    sensor.startContinuous(200000);
    
    """

    script += """
    digitalWrite(9, HIGH);
    digitalWrite(8, HIGH);
    analogWrite(3, initialMotorSpeed);
    analogWrite(11, initialMotorSpeed);
}
"""

    script += """
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
"""

    if literal_eval(config["HARDWARE"]["charger"]):
        script += """
    if (9.00 >= voltage_get()) {
        // voltage check, if under or is 9 volts, open motor power supply MOSFET and switch power relay to external
        digitalWrite(2, LOW);
        digitalWrite(4, HIGH);
    }

    if (9.50 >= voltage_get() && 9 < voltage_get()) {
        // secondary voltage check, if over 9 volts but less than or equal to 9.5 volts, only close motor power supply
        digitalWrite(4, LOW);
    }

    if (voltage_get() > 9.50) {
        // if voltage is greater than 9.5, power is within in spec, close motor power supply MOSFET and switch relay to internal
        digitalWrite(2, HIGH);
        digitalWrite(4, LOW);
    }"""

    script += """
    if (Serial.available() > 0) {
        
        incomingData = Serial.read();

        if (incomingData == 0x0A) { // 0x0A is the decimal code for a newline character, when it's received, the accumulator is dumped and evaluated
            accumulatorIndex = 0; // reset accumulator write index"""

    if literal_eval(config["HARDWARE"]["charger"]):
        script += """
            if (strcmp(accumulator, "*") == 0) {
                static char converted_voltage[5];
                dtostrf(voltage_get(), 5, 3, converted_voltage);
                Serial.write(converted_voltage);
                Serial.write("\\n");
            }"""

    script += """
            if (strcmp(accumulator, "(") == 0) {
                digitalWrite(2, HIGH);
            }
            
            if (strcmp(accumulator, ")") == 0) {
                digitalWrite(2, LOW);
            }
            
            if (strcmp(accumulator, "<") == 0) {
                digitalWrite(4, HIGH);
            }
            
            if (strcmp(accumulator, ">") == 0) {
                digitalWrite(4, LOW);
            }

            if (strcmp(accumulator, "F") == 0) {
                digitalWrite(12, LOW);
                digitalWrite(9, LOW);

                digitalWrite(13, HIGH);
                digitalWrite(8, LOW);
            }

            if (strcmp(accumulator, "B") == 0) {
                digitalWrite(12, HIGH);
                digitalWrite(9, LOW);

                digitalWrite(13, LOW);
                digitalWrite(8, LOW);
            }

            if (strcmp(accumulator, "A") == 0) {
                digitalWrite(9, HIGH);

                digitalWrite(8, HIGH);
            }

            if (strcmp(accumulator, "Z") == 0) {
                digitalWrite(13, LOW);
                digitalWrite(8, LOW);

                digitalWrite(9, HIGH);
            }

            if (strcmp(accumulator, "Y") == 0) {
                digitalWrite(13, HIGH);
                digitalWrite(8, LOW);

                digitalWrite(9, HIGH);
            }

            if (strcmp(accumulator, "X") == 0) {
                digitalWrite(8, HIGH);
                
                digitalWrite(12, HIGH);
                digitalWrite(9, LOW);
            }

            if (strcmp(accumulator, "W") == 0) {
                digitalWrite(8, HIGH);
                
                digitalWrite(12, LOW);
                digitalWrite(9, LOW);
            }

            if (strcmp(accumulator, "S") == 0) {
                digitalWrite(13, HIGH);
                digitalWrite(8, LOW);
                
                digitalWrite(12, HIGH);
                digitalWrite(9, LOW);
            }

            if (strcmp(accumulator, "C") == 0) {
                digitalWrite(13, LOW);
                digitalWrite(8, LOW);
                
                digitalWrite(12, LOW);
                digitalWrite(9, LOW);
            }
            """

    script += """
            if (strcmp(accumulator, "T") == 0) {
                Serial.print(sensor.readRangeSingleMillimeters());
                if (sensor.timeoutOccurred()) {
                    Serial.write("TIMEOUT");
                }
                Serial.write("\n");
            }
            
            """

    script += """
            char conditionalMotorSpeedChange[3] = {accumulator[0], accumulator[1]};

            if (strcmp(conditionalMotorSpeedChange, "MS") == 0) {
                char inputMotorSpeed[4] = {accumulator[3], accumulator[4], accumulator[5]};
                digitalWrite(9, HIGH);
                digitalWrite(8, HIGH);
                analogWrite(11, atoi(inputMotorSpeed));
                analogWrite(3, atoi(inputMotorSpeed));
            }

            memset(accumulator, 0, sizeof(accumulator)); // clears array.
        }
        else {
            if (accumulatorIndex <= 63) {
                accumulator[accumulatorIndex] = incomingData;
                accumulatorIndex += 1;
            }
        }
    }
}
    """
    script_export.write(script)
pass

print("Script generated. Please upload file to Arduino board.")
