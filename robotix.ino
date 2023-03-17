#define speedL 10
#define IN1 9
#define IN2 8 
#define IN3 7
#define IN4 6
#define speedR 5
#define sensorL 4
#define sensorR 3
int sl=0;
int sr=0;
void setup(){
  for(int i=5;i<=10;i++)
  {
    pinMode(i,OUTPUT);
  }
    pinMode(sensorR,INPUT);
    pinMode(sensorL,INPUT);
}
void forword()
{
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
  analogWrite(speedL,85);
  analogWrite(speedR,85);
}
void left()
{
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
  analogWrite(speedL,0);
  analogWrite(speedR,85);
delay(10);
}
void right()
{
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,LOW);
  analogWrite(speedL,85);
  analogWrite(speedR,0);
  delay(10);
}
void stopp(){
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,LOW);
  analogWrite(speedL,0);
  analogWrite(speedR,0);
}
void loop(){
  sl=digitalRead(sensorL);
  sr=digitalRead(sensorR);
  if(sl==0&&sr==0)
  forword();
  else if(sl==0&&sr==1)
  right();
  else if(sl==1&&sr==0)
  left();
  else if(sl==1&&sr==1)
  stopp(); }
