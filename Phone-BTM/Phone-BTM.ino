int input = '0';
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(8,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0)
  {
    input = (DEC)Serial.read();
    delay(250);
  }
}
