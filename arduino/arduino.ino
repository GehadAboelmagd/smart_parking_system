#include <Stepper.h>

// stepper
const int stepsPerRevolution = 200;
Stepper up_Stepper(stepsPerRevolution, 8, 9, 10, 11);
Stepper down_Stepper(stepsPerRevolution, 0, 1, 2, 3);
//

// step 
int floor_step[3] = {200,400,600};
int park_step[3] = {50,100,150};
//

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  up_Stepper.setSpeed(60);
  down_Stepper.setSpeed(60);  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    char c = Serial.read();
    if(c == 'P') parking();
    else if(c == 'G') get_car();
  }
}

void parking() {
  
}

void get_car(){
  while(!(Serial.available())){}
  int park_n = Serial.read();
  int f = park_n /3 , d = 50;
  int p = park_n %3; 
  up_Stepper.step(floor_step[f]-d);
  delay(1000);
  down_Stepper.step(park_step[p]);
  delay(1000);
  up_Stepper.step((floor_step[f+1]-floor_step[f]));
  delay(1000);
  down_Stepper.step(-park_step[p]);  
  delay(1000);  
  up_Stepper.step(-(floor_step[f+1]-d));  
  delay(1000);

  Serial.write('D');
  Serial.flush();  
}
