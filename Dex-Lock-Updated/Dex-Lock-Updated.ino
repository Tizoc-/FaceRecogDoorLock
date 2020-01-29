#include <Servo.h>

// Notiification LED (Red- Lock, Green-Unlock)
#define greenLED 31
#define redLED 46

//Unlock door from inside
#define unlockButton 30

//Servo Declaration
Servo myServo;
#define servPin 2

//Ultra Sonic Declaration
#define trigPin 5
#define echoPin 6

// Global Variables
long duration;
int distance;
bool lock = true;// false for unlock, true for lock,
char incomingByte = 0;

void setup() {
  //Use Serial Monitor for testing purposes
  //Serial.begin(9600);
  
  //Use Bluetooth for Raspberry Pi Signal
  Serial.begin(38400);

  //LED setup
  pinMode(greenLED,OUTPUT);
  pinMode(redLED,OUTPUT);

  //unlockButton 
  pinMode(unlockButton,INPUT_PULLUP);

  //Servo Setup
  myServo.attach(servPin);
  myServo.write(0);

  //Ultra Sonic Sensor
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT); 
}

void ultraSen()
{
  // put your main code here, to run repeatedly:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculating the distance
  distance = duration*0.0133/2;
}

//To Check the door after its been open
void lockState(bool islock,bool isPi)
{
  int counter = 0;
  
  // Setting to Lock when door is shut
  if(distance < 2 and islock == false)
  {
    delay(50);
    while(distance < 2 )
    {
      delay(1000);
      counter++;
      if(counter >= 5)
      {
        //Turn Red LED for Lock
        setLED(redLED,0);
        setLED(greenLED,0);
        
        myServo.write(83);
        delay(300);
        setLED(redLED,1);
        setLED(greenLED,0);
        lock = true;
        counter = 0;
        break;
      }
    }
  }
  
  //Setting to Unlock when door is opened
  else if(distance > 2 and islock == true)
  {
    delay(50);
    while(distance >= 2)
    {
      delay(1000);
      counter++;
      if(counter >= 5)
      {
        //Turn Green LED for unlock
        setLED(redLED,0);
        setLED(greenLED,0);
        myServo.write(0);
        delay(500);
        setLED(redLED,0);
        setLED(greenLED,1);
        lock = false;
        counter = 0;
        break;
      }
    }
  }
  //If Pi send a signal
  else if(isPi == true)
  {
      delay(50);
      //Turn Green LED for unlock
      setLED(redLED,0);
      setLED(greenLED,0);
      myServo.write(0);
      delay(500);
      setLED(redLED,0);
      setLED(greenLED,1);
  }

  //Inside Button Press
  else if(lock == true and digitalRead(unlockButton) == HIGH)
  {
    delay(50);
    setLED(greenLED,0);
    setLED(redLED,0);
    myServo.write(0);
    delay(500);
    setLED(greenLED,1);
    setLED(redLED,0);
    //lock = false;
  }
}

void setLED(int LED, int onOff)
{
  digitalWrite(LED,onOff);
}

void cout(int x)
{
  Serial.println(x);
}

void loop() {
  if(Serial.available()>0);
  {
    incomingByte = Serial.read();
    //Serial.println(incomingByte,DEC);
    Serial.println(incomingByte);
    delay(1000);
    if(incomingByte == '2' and lock == true and distance < 2)
    {
      lockState(lock,true);
      //5 Seconds to open door
      delay(5000);
    }
  }
  ultraSen();
  lockState(lock,false);
  //cout(distance);
  //cout(digitalRead(unlockButton));

}
