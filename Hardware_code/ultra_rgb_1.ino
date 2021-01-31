#include <Servo.h>
#include <Wire.h>

#define Trig 2 //引脚Tring 连接 IO D3
#define Echo 3 //引脚Echo 连接 IO D2

#define redPin 5 // red
#define grePin 6 // green
#define bluPin 7 // blue

#define rPin 8 // red
#define gPin 9 // green
#define bPin 10 // blue

#define servo 11
#define Switch 12

#define buzz 13 // passive Buzzer
#define SLAVE_ADDRESS 0x04

Servo myservo; // create servo object to control a servo

int pos = 0; // variable to store the servo position

float cm; //距离变量
float temp; // 
int count = 0; 
int instruction = 0;

int data_s;
int data_r;

void setup() 
{
  Serial.begin(9600); // 9600 bps
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);//从机 接收 主机 发来的数据
  Wire.onRequest(sendData); //从机 请求 主机 发送数据
  Serial.println("Ready");
  
  // set up for RGB
  pinMode(redPin, OUTPUT);
  pinMode(grePin, OUTPUT);
  pinMode(bluPin, OUTPUT);
  pinMode(rPin, OUTPUT);
  pinMode(gPin, OUTPUT);
  pinMode(bPin, OUTPUT);
  // set up for Ultrasonic
  pinMode(Trig, OUTPUT);
  pinMode(Echo, INPUT);
  //pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  myservo.attach(servo); // attaches the servo on pin 11 to the servo object

  pinMode(buzz, OUTPUT); // buzzer
  digitalWrite(rPin, HIGH); // red    unavailable
  digitalWrite(gPin, HIGH);
  digitalWrite(bPin, HIGH);
  delay(1000);
}

void loop()
{ 
  //给Trig发送一个低高低的短时间脉冲,触发测距
  digitalWrite(Trig, LOW); //给Trig发送一个低电平
  delayMicroseconds(2);    //等待 2微妙
  digitalWrite(Trig,HIGH); //给Trig发送一个高电平
  delayMicroseconds(10);    //等待 10微妙
  digitalWrite(Trig, LOW); //给Trig发送一个低电平

  float distance = pulseIn(Echo, HIGH) / 58.0; //或者 / 58.0 也可以 
  distance = (int (distance * 100.0) ) / 100.0; 
  
  led_buzz_module(digitalRead(Switch));
  led_module_r_g(distance);

  instruction = data_r;
  servo_module(instruction); 
  Serial.print(distance);//串口输出距离换算成cm的结果
  Serial.println("cm");
}

void setColor(int red, int green, int blue)
{
 analogWrite(redPin, red);
 analogWrite(grePin, green);
 analogWrite(bluPin, blue);
}

void led_buzz_module(bool sw){
  if (sw == 0){ //
    Serial.println("Opened");  
    digitalWrite(LED_BUILTIN, HIGH);
    // setColor(255, 24, 148); // pink.purple
    // setColor(80, 0, 80); // blue
    digitalWrite(redPin, HIGH);
    digitalWrite(grePin, HIGH);
    digitalWrite(bluPin, HIGH);
    //setColor(0, 255, 255); // aqua
    setColor(255, 24, 148);
    analogWrite(buzz, LOW); // buzzer
    delay(2000);
    analogWrite(buzz, HIGH);
  }
  else {
    Serial.println("Closed");  
    digitalWrite(LED_BUILTIN, LOW);
    //setColor(255, 255, 125); // raspberry color
    //setColor(255, 24, 148);
    digitalWrite(redPin, LOW);
    digitalWrite(grePin, LOW);
    digitalWrite(bluPin, LOW);
    analogWrite(buzz, HIGH); // buzzer
  }
}

void led_module_r_g(float distance){
  if (distance <= 25){ // when there is something inside
    count++;
    if (count < 5){
      digitalWrite(rPin, LOW); // red    unavailable
      digitalWrite(gPin, HIGH);
      digitalWrite(bPin, HIGH);
      digitalWrite(2, LOW);
      count = 0;
      data_s = 1;
    }
  }
  else {
    digitalWrite(rPin, HIGH);
    digitalWrite(gPin, LOW); // green   available/empty
    digitalWrite(bPin, HIGH);
    digitalWrite(2, HIGH);
    data_s = 0;
  }
}
void servo_module(int instructon){
  if(instruction == 1){
    myservo.write(90);
  }
  else{
    myservo.write(0);
  }
}

// callback for received data
void receiveData(int byteCount){
  while(Wire.available()) {
  data_r = Wire.read();
  Serial.print("data received: "); // 2/1 for lock/unlock
  Serial.println(data_r);
  }
}
// callback for sending data
void sendData(){
  Wire.write(data_s); // 0/1 for empty or occupy
}
