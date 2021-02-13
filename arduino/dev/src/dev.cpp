// Raspbot Remote Control Application, Arduino Instructions for Serial Commandment
// See documentation on pinouts and additional information.

// development script

#include <Arduino.h>

// Variable Declaration
int incomingData;
int accumulatorIndex = 0;
char accumulator[64]; 
int initialMotorSpeed = 90; // must be 0-255
                       
static float voltage_get() {
    float raw = analogRead(5);
    return ((raw * 5.0000000) / 1024.000000) / (7.50/37.50);
}

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
    
    if (voltage_get() > 9.50) {
        // if battery voltage over 9.5, close motor power supply MOSFET and switch power relay to internal
        digitalWrite(2, HIGH);
        digitalWrite(4, LOW);
    }
    else {
        digitalWrite(2, LOW);
        digitalWrite(4, HIGH);
    }

    digitalWrite(9, HIGH);
    digitalWrite(8, HIGH);
    analogWrite(3, initialMotorSpeed);
    analogWrite(11, initialMotorSpeed);
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
    }

    if (Serial.available() > 0) {
        
        incomingData = Serial.read();

        if (incomingData == 0x0A) { // 0x0A is the decimal code for a newline character, when it's received, the accumulator is dumped and evaluated
            accumulatorIndex = 0; // reset accumulator write index

            if (strcmp(accumulator, "*") == 0) {
                static char converted_voltage[5];
                dtostrf(voltage_get(), 5, 3, converted_voltage);
                Serial.write(converted_voltage);
                Serial.write("\n");
            }
            
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
                digitalWrite(13, HIGH);
                digitalWrite(8, LOW);
                
                digitalWrite(12, LOW);
                digitalWrite(9, LOW);
            }

            if (strcmp(accumulator, "T") == 0) {
                Serial.write("9999\n"); // TODO time-of-flight distance sensor
            }

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
