#include<AFMotor.h>

AF_Stepper motor_1(200,1);  
//motor_1 is dedicated for vertical motion
//motor_1 is connected to M1,M2(port 1)
AF_Stepper motor_2(200,2);
//motor_2 is dedicated for rotational motion
//motor_2 is connected to M3,M4(port 2)

void prepare_for_parking(int x);
void parking(int x);
void reverse_parking(int x);
void up_draw_down(int x);
void up_park_draw_down(int x, int y);

//initially, there is no platform in the waiting hall (after a getcar operation) to bring it back 
int flag=0;
//initially there is no park_n without platform
int without_platform_n=0;

// step 
int floor_step[4] = {0,200,400,600};
int park_step[3] = {50,100,150};
//

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

    switch (parking_order)
    {
      case '1':
        prepare_for_parking(park_n);
        break;
      case '2':
        parking(park_n); 
        break;
      case '3':
        reverse_parking(park_n);
        break;   
    }
  }
}


void prepare_for_parking(int x)
{
  if (flag==0)
  {
    up_draw_down(x);
  }
  
  else if (flag==1)
  {
    if (x==without_platform_n)
    ;//do nothing
    else 
    up_park_draw_down(without_platform_n,x);
  }

  //  flag=0;
  //  without_platform_n=0;
  
  Serial.write('D');
  Serial.flush();
}


void parking(int x)
{
  int i = (x-1)/3 +1;
  int j = (x-1)%3;
  motor_1.step((floor_step[i+1]+floor_step[i])/2 ,FORWARD,SINGLE);    delay(1000);
  motor_2.step(park_step[j],FORWARD,SINGLE);                          delay(1000);
  motor_1.step((floor_step[i+1]-floor_step[i-1])/2 ,BACKWARD,SINGLE); delay(1000);
  motor_2.step(park_step[j],BACKWARD,SINGLE);                         delay(1000);
  motor_1.step((floor_step[i]+floor_step[i-1])/2 ,BACKWARD,SINGLE);   delay(1000);

  flag=0;
  without_platform_n=0;
  Serial.write('D');
  Serial.flush();
}


void reverse_parking(int x)
{
  if (flag==0)
  up_draw_down(x);

  else if (flag==1)
  up_park_draw_down(without_platform_n,x);

  flag=1;
  without_platform_n=x;

  Serial.write('D');
  Serial.flush();
}


void up_draw_down(int x)
{
  int i = (x-1)/3 +1;
  int j = (x-1)%3;
  motor_1.step((floor_step[i]+floor_step[i-1])/2 ,FORWARD,SINGLE);    delay(1000);
  motor_2.step(park_step[j],FORWARD,SINGLE);                          delay(1000);
  motor_1.step((floor_step[i+1]-floor_step[i-1])/2 ,FORWARD,SINGLE);  delay(1000);
  motor_2.step(park_step[j],BACKWARD,SINGLE);                         delay(1000);
  motor_1.step((floor_step[i+1]+floor_step[i])/2 ,BACKWARD,SINGLE);   delay(1000);
}



void up_park_draw_down(int x, int y)
{
  //park variable(x) and draw variable(y)
  
  int i = (x-1)/3 +1;   int j = (x-1)%3;
  int m = (y-1)/3 +1;   int n = (y-1)%3;  
  
  motor_1.step((floor_step[i+1]+floor_step[i])/2 ,FORWARD,SINGLE);    delay(1000);
  motor_2.step(park_step[j],FORWARD,SINGLE);                          delay(1000);
  motor_1.step((floor_step[i+1]-floor_step[i-1])/2 ,BACKWARD,SINGLE); delay(1000);
  //now the unwanted platform is parked and the fork is under without_platform_n
  
  if(i==m) //the same floor
  {
    if(n>j)
    motor_2.step(park_step[n]-park_step[j] ,FORWARD,SINGLE);
    else if (n<j)
    motor_2.step(park_step[j]-park_step[n] ,BACKWARD,SINGLE);
    delay(1000);
  }

  else //(i!=m)
  {
    motor_2.step(park_step[j],BACKWARD,SINGLE);                       
    delay(1000);
    
    if (m>i)
    motor_1.step(( floor_step[m]+floor_step[m-1]-floor_step[i]-floor_step[i-1] )/2 ,FORWARD,SINGLE);
    else  //(m<i)
    motor_1.step(( floor_step[i]+floor_step[i-1]-floor_step[m]-floor_step[m-1] )/2 ,BACKWARD,SINGLE);
    delay(1000);
    
    motor_2.step(park_step[n],FORWARD,SINGLE);  
    delay(1000);
  }

  //now the fork is under the wanted platform

  motor_1.step((floor_step[m+1]-floor_step[m-1])/2 ,FORWARD,SINGLE);  delay(1000);
  motor_2.step(park_step[n],BACKWARD,SINGLE);                         delay(1000);
  motor_1.step((floor_step[m+1]+floor_step[m])/2 ,BACKWARD,SINGLE);   delay(1000);
}
