#include<AFMotor.h>

AF_Stepper motor_1(200,1);  
//motor_1 is dedicated for vertical motion
//motor_1 is connected to M1,M2(port 1)
AF_Stepper motor_2(200,2);
//motor_2 is dedicated for rotational motion
//motor_2 is connected to M3,M4(port 2)

void parking(int x,int y);
void reverse_parking(int x);

//initially the first place has no platform
int without_platform_n=1;
//initially the first place is where we should park
int flag=0;

void setup()
{
  Serial.begin(9600);
  motor_1.setSpeed(10); //10 rpm or maybe modified
  motor_2.setSpeed(10); // may be modified
  
}


void loop()
{
  if(Serial.available())
  {
    char parking_order=Serial.read();
    while(!Serial.available()) {}
    int park_n=Serial.read();
    // 1,2,3 for the 1st floor and 4,5,6 for 2nd floor, and so on
    
    if(parking_order=='1')
    {
      while(!Serial.available()) {}
      int next_park_n=Serial.read();
      parking(park_n,next_park_n);
    }
    
    else if (parking_order=='2')
    reverse_parking(park_n);     
  }
}



void parking(int x,int y)
{
  if(x!=without_platform_n)
  {
    flag=1;
    parking(without_platform_n , x);    
  }
  int coef=4; // or may be changed
  //let number of rotations to translate 1 floor(20 cm) is 4 rotations
  // 1 rotation = 5cm = 2*pi*r

  int i = (x-1)/3; int j=(x-1)%3;
  int m = (y-1)/3; int n=(y-1)%3;  
   
  //code for parking the car 
  motor_1.step((i+1.5)*200*coef,FORWARD,SINGLE);    delay(1000); 
  motor_2.step(50*(j+1),FORWARD,SINGLE);            delay(1000);
  motor_1.step(200*coef,BACKWARD,SINGLE);           delay(1000); 
  //now the fork is under the park_n
  
  if (y!=0)   //there is a next_park_n available
  {
    //code for setting the fork to be under the next_park_n
    if(m==i)
    {
      if (n>j) motor_2.step(50*(n-j),FORWARD,SINGLE);
      else 
      if (n<j) motor_2.step(50*(j-n),BACKWARD,SINGLE);
      delay(1000);
    }
  
    else
    {
      motor_2.step(50*(j+1),BACKWARD,SINGLE);         delay (1000);
      if(m>i)  motor_1.step((m-i)*200*coef,FORWARD,SINGLE);
      else
      if(m<i)  motor_1.step((i-m)*200*coef,BACKWARD,SINGLE);
      delay(1000);
      motor_2.step(50*(n+1),FORWARD,SINGLE);          delay(1000);
    }
    //now the fork is under the next_park_n
  
    //code for going back to the wait hall
    motor_1.step(200*coef,FORWARD,SINGLE);            delay(1000);
    motor_2.step(50*(n+1),BACKWARD,SINGLE);           delay(1000);
    motor_1.step((m+1.5)*200*coef,BACKWARD,SINGLE);   delay(1000);
    without_platform_n= y; 
  }

  else if (y==0) //there is no next_park_n available
  {
    motor_2.step(50*(j+1),BACKWARD,SINGLE);           delay(1000);
    motor_1.step((i+.5)*200*coef,BACKWARD,SINGLE);    delay(1000);
    without_platform_n=0;
  }
  
  if(flag!=1)
  {
     Serial.write('D');
     Serial.flush();
  }

  flag=0;
}


void reverse_parking(int x)
{
  if(without_platform_n!=0)
  parking(without_platform_n,x);
  
  else if(without_platform_n==0)
  {
    int coef=4; // or may be changed
    //let number of rotations to translate 1 floor(20 cm) is 4 rotations
    // 1 rotation = 5cm = 2*pi*r
    int i = (x-1)/3; int j=(x-1)%3;
    motor_1.step((i+.5)*200*coef,FORWARD,SINGLE);     delay(1000); 
    motor_2.step(50*(j+1),FORWARD,SINGLE);            delay(1000);
    motor_1.step(200*coef,FORWARD,SINGLE);            delay(1000); 
    motor_2.step(50*(j+1),BACKWARD,SINGLE);           delay(1000);
    motor_1.step((i+1.5)*200*coef,BACKWARD,SINGLE);   delay(1000);
    
    without_platform_n=x;
    Serial.write('D');
    Serial.flush();
  }
}
