#include<AFMotor.h>

const int stepsPerRevolution = 200;
AF_Stepper motor_1(stepsPerRevolution,1);  
//motor_1 is dedicated for vertical motion
//motor_1 is connected to M1,M2(port 1)
AF_Stepper motor_2(stepsPerRevolution,2);
//motor_2 is dedicated for rotational motion
//motor_2 is connected to M3,M4(port 2)

// step 
int floor_step[4] = {0,930,2010,2600};
int park_step[3] = {52,100,150};
//

void prepare_for_parking(int x);
void parking(int x);
void reverse_parking(int x);
void up_draw_down(int x);
void transfer_draw_down(int x);
void up_park_draw_down(int x, int y);
void neat_turn_f(int x);
void neat_turn_b(int x);

int flag=0;  //initially, the system is at startup
//flag is used to keep track of the last operation
//flag=1 if the last operation is parking a client car (the fork is under park_n with no platform)
//flag=2 if the last operation is getting a client car (the fork is at the hall with a platform on it)

int without_platform_n=0;   //initially there is no park_n without platform

int fork_floor_step=0;  //after a parking operation, the fork_floor_step is always under some park_n 
int fork_park_step=0;



void setup()
{
  Serial.begin(9600);
  motor_1.setSpeed(30); //10 rpm or maybe modified
  motor_2.setSpeed(5); // may be modified
  
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
  switch (flag)
  {
    case 0:
      up_draw_down(x);
      break;
    case 1:
      transfer_draw_down(x);
      break;
    case 2:
      if(without_platform_n != x)
      up_park_draw_down(without_platform_n,x);
      break;
  }

  //  flag=2;
  //  without_platform_n=x;
  //  fork_floor_step=0;
  //  fork_park_step=0;
  
  Serial.write('D');
  Serial.flush();
}


void parking(int x)
{
  int i = (x-1)/3 +1;
  int j = (x-1)%3;
  motor_1.step((floor_step[i+1]+floor_step[i])/2 ,FORWARD,SINGLE);    delay(1000);
  neat_turn_f(park_step[j]);                                          delay(1000);
  motor_1.step((floor_step[i+1]-floor_step[i-1])/2 ,BACKWARD,SINGLE); delay(1000);

  flag=1;
//  without_platform_n=0;
  fork_floor_step = (floor_step[i]+floor_step[i-1])/2;
  fork_park_step = park_step[j]; 
  
  Serial.write('D');
  Serial.flush();
}


void reverse_parking(int x)
{
  switch (flag)
  {
    case 1:
      transfer_draw_down(x);
      break;
    case 2:
      up_park_draw_down(without_platform_n,x);
      break;
  }

  flag=2;
  without_platform_n=x;
//  fork_floor_step=0;
//  fork_park_step=0;

  Serial.write('D');
  Serial.flush();
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  


void up_draw_down(int x)
{
  int i = (x-1)/3 +1;
  int j = (x-1)%3;
  motor_1.step((floor_step[i]+floor_step[i-1])/2 ,FORWARD,DOUBLE);    delay(1000);
  neat_turn_f(park_step[j]);                                          delay(1000);
  motor_1.step((floor_step[i+1]-floor_step[i-1])/2 ,FORWARD,DOUBLE);  delay(1000);
  neat_turn_b(park_step[j]);                                          delay(1000);
  motor_1.step((floor_step[i+1]+floor_step[i])/2 ,BACKWARD,DOUBLE);   delay(1000);
}


void transfer_draw_down(int x)
{
  int i = (x-1)/3 +1;  //floor_step_index
  int j = (x-1)%3;     //park_step_index
  
  if(fork_floor_step == ((floor_step[i]+floor_step[i-1])/2))  //the same floor
  {
    if(fork_park_step < park_step[j])
    motor_2.step( park_step[j] - fork_park_step,FORWARD,SINGLE);
    else if(fork_park_step > park_step[j])
    motor_2.step(fork_park_step - park_step[j] ,BACKWARD,SINGLE);
    delay(1000); 
    //if the park_step[j] is the same as fork_park_step: do nothing
  }
  else 
  {
    neat_turn_b(fork_park_step);  
    delay(1000);
    
    if( fork_floor_step < ((floor_step[i]+floor_step[i-1])/2) )
    motor_1.step( ((floor_step[i]+floor_step[i-1])/2) - fork_floor_step,FORWARD,SINGLE);
    else
    motor_1.step( fork_floor_step - ((floor_step[i]+floor_step[i-1])/2) ,BACKWARD,SINGLE);
    delay(1000);
    neat_turn_f(park_step[j]);   
    delay(1000); 
  }

  //now the fork is under the desired platform
  
  motor_1.step((floor_step[i+1]-floor_step[i-1])/2 ,FORWARD,SINGLE);  
  delay(1000);
  neat_turn_b(park_step[j]);                         
  delay(1000);
  motor_1.step((floor_step[i+1]+floor_step[i])/2 ,BACKWARD,SINGLE);   
  delay(1000);
}


void up_park_draw_down(int x, int y)
{
  //park variable(x) and draw variable(y)
  
  int i = (x-1)/3 +1;   int j = (x-1)%3;
  int m = (y-1)/3 +1;   int n = (y-1)%3;  
  
  motor_1.step((floor_step[i+1]+floor_step[i])/2 ,FORWARD,SINGLE);    delay(1000);
  neat_turn_f(park_step[j]);                                          delay(1000);
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
    neat_turn_b(park_step[j]);                      
    delay(1000);
    
    if (m>i)
    motor_1.step(( floor_step[m]+floor_step[m-1]-floor_step[i]-floor_step[i-1] )/2 ,FORWARD,SINGLE);
    else  //(m<i)
    motor_1.step(( floor_step[i]+floor_step[i-1]-floor_step[m]-floor_step[m-1] )/2 ,BACKWARD,SINGLE);
    delay(1000);

    neat_turn_f(park_step[n]);
    delay(1000);
  }

  //now the fork is under the wanted platform

  motor_1.step((floor_step[m+1]-floor_step[m-1])/2 ,FORWARD,SINGLE);  delay(1000);
  neat_turn_b(park_step[n]);                        delay(1000);
  motor_1.step((floor_step[m+1]+floor_step[m])/2 ,BACKWARD,SINGLE);   delay(1000);
}

void neat_turn_f(int x)
{
  if(x< (stepsPerRevolution/2) )
  motor_2.step(x,FORWARD,SINGLE);
  else
  motor_2.step(stepsPerRevolution-x,BACKWARD,SINGLE);
}

void neat_turn_b(int x)
{
  if(x< (stepsPerRevolution/2) )
  motor_2.step(x,BACKWARD,SINGLE);
  else
  motor_2.step(stepsPerRevolution-x,FORWARD,SINGLE);
}
