#include <LiquidCrystal.h>
#include <Servo.h>

// Creates an LCD object. Parameters: (rs, enable, d4, d5, ~d6, ~d7)
const int rs = 6, en = 5, d4 = 52, d5 = 53, d6 = 4, d7 = 3;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//Ultra Sonic Sensor
const int trigPin = 13;
const int echoPin = 12;

//Servo and Degrees
const int servPin = 2;
const int analogPin = A15;
double degree = 0;
Servo serv;

//LCD Calculation
long duration;
int distance;
int distD,distP = 0;

//LED pins
const int Yellow = 50;
const int Green = 48;

//Set Buttons
const int setDist = 51;
const int gotPackage = 46;

int timer = 0;
//bool packageSet = false;

void setup() 
{
  // Ultra Sonic
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  
  //Variable Resister Servo
  pinMode(analogPin,INPUT);
  serv.attach(servPin);
  
  //LCD
  lcd.begin(16,2);

  //Set Buttons
  pinMode(gotPackage, INPUT);
  pinMode(setDist, INPUT);

  //LED Pins
  pinMode(Yellow, OUTPUT);
  pinMode(Green, OUTPUT);

  //Serial
  //Serial.begin(9600);

}
void setDefDist()
{
    while(digitalRead(setDist) == HIGH)//Reset Distance
    {
      if(timer == 3)
      {
        break;
      }
      timer++;
      delay(3000);
    }
    if(timer == 3)
    {
      distD = 0;
      timer = 0;
    }
    else if(distD == 0 and timer < 2) 
    {
      distD = distance;
      timer = 0;
    }
    delay(1500);
}
void setPackage()
{
  while(distD > distance)
    {
      if(timer == 3)
      {
        digitalWrite(Green,HIGH);
        digitalWrite(Yellow,LOW);
        serv.write(108);
        distP = distance;
        timer = 0;
        break;
      }
      timer++;
      delay(1000);
    }
}
void packageFinder()
{
  while(distP < distance)
    {
      if(timer == 3)
      {
        digitalWrite(Green,LOW);
        digitalWrite(Yellow,HIGH);
        serv.write(70);
        delay(1000);
        serv.write(160);
        delay(1000);
        serv.write(108);
        break;
      }
      timer++;
      delay(1000);
    }
}
void LcdDisp()
{
  lcd.clear();
  lcd.setCursor(0,0); // Sets the location at which subsequent text written to the LCD will be displayed
  lcd.print("Dist:"); // Prints string "Distance" on the LCD
  lcd.print(distance); // Prints the distance value from the sensor
  lcd.setCursor(0,1);
  lcd.print("Default:");
  lcd.print(distD);
  lcd.setCursor(8,0);
  lcd.print("Pack:");
  lcd.print(distP);
  delay(250);
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
void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(setDist) == HIGH)
  {
    setDefDist();
  }
  if(distD > distance and distD != 0)
  {
    setPackage();
  }
  if(distP < distance and distP !=0 and digitalRead(Yellow) == LOW)
  {
    packageFinder();
  }
  if(digitalRead(gotPackage) == HIGH and distP != 0)
  {
    digitalWrite(Green,LOW);
    digitalWrite(Yellow,LOW);
    serv.write(0);
    distP = 0;
  }
  ultraSen();
  LcdDisp();

}
