// Raspbot Remote Control Motor Executer
// Performs navigation tasks as per requested through serial

// 12 and 9 -> MotorDirection and Brake for A
// 13 and 8 -> MotorDirection and Brake for B
// 3 -> Analog motor speed input for A
// 11 -> Analog motor speed input for B

int incomingData;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(12, OUTPUT);
  pinMode(9, OUTPUT);
  
  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly: 
  if (Serial.available() > 0) {
     
    incomingData = Serial.read();
    
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
  }
}


