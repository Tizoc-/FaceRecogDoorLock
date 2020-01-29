 #include <Servo.h>

Servo myServo;
int input;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  myServo.attach(3);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0)
  {
    input = Serial.parseInt();
    myServo.write(input);
    Serial.println(input);
    delay(3000);
    
  }
}
