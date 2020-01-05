
// Raspbot Remote Control Application (Raspbot RCA-G), Arduino Instructions for Serial Commandment
// Secondary Arduino Instructions for Nano, a part of Upgrade #1 Set, controlling power systems.

// A0 -> Battery Voltage Sensor


int incomingData;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // key
  // & = Compatability Check
  // * = Voltage Check (Upgrade #1)

  if (Serial.available() > 0) {

    incomingData = Serial.read();

    if (incomingData == '&') {
      // TODO hardware check here
    }

    if (incomingData == '*') {
      int value = analogRead(A0);
      float voltage = value * (5.0 / 1023.0);
      Serial.println(voltage);
      // Serial.write(voltage);
      // Serial.write('\n')
    }
  }
}
