//                        Coder : ENG.Mahmoud | Eng.Gehad
//                        Version : v2.0B
//                        version Date :  19 / 5 / 2023
//                        Code Type : arduino C++ 
//                        Title : Smart Parking System
//                        Interpreter : cGNU C++ compiler  (C++11)


#include <AFMotor.h>

// stepper
const int stepsPerRevolution = 200;
AF_Stepper up_Stepper(stepsPerRevolution, 1);
AF_Stepper down_Stepper(stepsPerRevolution, 2);
//

// step 
int floor_step[4] = {0,200,400,600};
int park_step[3] = {50,100,150};
//

void parking();
void reverse_parking();

void setup() {

  Serial.begin(9600);
  up_Stepper.setSpeed(60);
  down_Stepper.setSpeed(60);  
}

void loop() {

  if(Serial.available()){
    char c = Serial.read();
    if(c == '1') parking();
    else if(c == '2') reverse_parking();
  }
}

void parking() {
  while(!(Serial.available())){}
  int park_n = Serial.read();
  int f = (park_n /3)+1 , d = 50;
  int p = park_n %3; 
  up_Stepper.step(floor_step[f]+d,FORWARD,SINGLE);
  delay(1000);
  down_Stepper.step(park_step[p],FORWARD,SINGLE);
  delay(1000);
  up_Stepper.step((floor_step[f]-floor_step[f-1]),BACKWARD,SINGLE);
  delay(1000);
  down_Stepper.step(park_step[p],BACKWARD,SINGLE);  
  delay(1000);  
  up_Stepper.step((floor_step[f-1]+d),BACKWARD,SINGLE);  
  delay(1000);

  Serial.write('D');
  Serial.flush(); 
}

void reverse_parking(){
  while(!(Serial.available())){}
  int park_n = Serial.read();
  int f = (park_n /3)+1 , d = 50;
  int p = park_n %3; 
  up_Stepper.step(floor_step[f]-d,FORWARD,SINGLE);
  delay(1000);
  down_Stepper.step(park_step[p],FORWARD,SINGLE);
  delay(1000);
  up_Stepper.step((floor_step[f+1]-floor_step[f]),FORWARD,SINGLE);
  delay(1000);
  down_Stepper.step(park_step[p],BACKWARD,SINGLE);  
  delay(1000);  
  up_Stepper.step((floor_step[f+1]-d),BACKWARD,SINGLE);  
  delay(1000);

  Serial.write('D');
  Serial.flush();
}