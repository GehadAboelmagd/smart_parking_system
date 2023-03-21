#include<AFMotor.h>

AF_Stepper motor_1(200,1);  
//motor_1 is dedicated for vertical motion
//motor_1 is connected to M1,M2(port 1)
AF_Stepper motor_2(200,2);
//motor_2 is dedicated for rotational motion
//motor_2 is connected to M3,M4(port 2)

void parking(int x);
void reverse_parking(int x);

void setup()
{
  Serial.begin(9600);
  motor_1.setSpeed(10); //10 rpm or maybe modified
  motor_2.setSpeed(10); // may be modified
}


void loop()
{
  if(Serial.available()>0)
  {
    char parking_order=Serial.read();
    int parking_place=Serial.read();  
    // 1,2,3 for the 1st floor and 4,5,6 for 2nd floor 
    if (parking_order=='1')        
    parking(parking_place);
    else if (parking_order=='2')   
    reverse_parking(parking_place);
  }
}

void parking(int x)
{
  int coef=4; // or may be changed
  //let number of rotations to translate 1 floor(20 cm) is 4 rotations
  // 1 rotation = 5cm = 2*pi*r
  int i = (x-1)/3; j=(x-1)%3;
  motor_1.step((i+1.5)*200*coef,FORWARD,SINGLE);    delay(1000); 
  motor_2.step(50*(j+1),FORWARD,SINGLE);            delay(1000);
  motor_1.step(200*coef,BACKWARD,SINGLE);           delay(1000); 
  motor_2.step(50*(j+1),BACKWARD,SINGLE);           delay(1000);
  motor_1.step((i+.5)*200*coef,BACKWARD,SINGLE);
}


void reverse_parking(int parking_place)
{
  int coef=4; // or may be changed
  //let number of rotations to translate 1 floor(20 cm) is 4 rotations
  // 1 rotation = 5cm = 2*pi*r
  int i = (x-1)/3; j=(x-1)%3;
  motor_1.step((i+.5)*200*coef,FORWARD,SINGLE);    delay(1000); 
  motor_2.step(50*(j+1),FORWARD,SINGLE);            delay(1000);
  motor_1.step(200*coef,FORWARD,SINGLE);           delay(1000); 
  motor_2.step(50*(j+1),BACKWARD,SINGLE);           delay(1000);
  motor_1.step((i+1.5)*200*coef,BACKWARD,SINGLE);
}
