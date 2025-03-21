int PWMA = 13;
int PWMB = 12;
int AIN2 = 3;
int AIN1 = 2;
int BIN1 = 5;
int BIN2 = 6;
//int STBY = 5;
#define ledPin 13
#define digitalPin1 32 //前置命令定義 analogPin 來自於 A0
#define digitalPin2 34
#define digitalPin3 36
#define digitalPin4 38
#define digitalPin5 40



void setup() {
  // put your setup code here, to run once:
  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(digitalPin1, INPUT);  // 目前預設該接腳作為輸入
  pinMode(digitalPin2, INPUT);
  pinMode(digitalPin3, INPUT);
  pinMode(digitalPin4, INPUT);
  pinMode(digitalPin5, INPUT);

  Serial.begin(9600);  // 表示開始傳遞與接收序列埠資料
}

// int speedv1(int vl, int vr) {
//   int vl = vl* 1.2 = ;
//   return vl;
// }
// int speedv2(int v1, int vr) {
// }

void MotorWriting(double vL, double vR) {
  vR=vR*0.935;  
  if (vR >= 0) {
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    //這邊的Motor第幾個對應到的High/Low是助教的車對應到的，請自己測試自己車該怎麼填！
  } else if (vR < 0) {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
    vR = -vR;  //因為analogWrite只吃正數，所以如果本來是負數，就要乘-1
  }
  if (vL >= 0) {
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH);
    //這邊的Motor第幾個對應到的High/Low是助教的車對應到的，請自己測試自己車該怎麼填！
  } else if (vL < 0) {
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    vL = -vL;  //因為analogWrite只吃正數，所以如果本來是負數，就要乘-1
  }
  analogWrite(PWMB, (int)vL);
  analogWrite(PWMA, (int)vR);
}


// void uturn(double v,int l3, int l2, int m, int r2, int r3){
  
// }

void Tracking(double v) {
  int w2 = 1.1;
  int w3 = 1.2;
  int Tp = v;
  int Kp = Tp*0.5;
  int l3 = digitalRead(digitalPin1);
  int l2 = digitalRead(digitalPin2);
  int m = digitalRead(digitalPin3);
  int r2 = digitalRead(digitalPin4);
  int r3 = digitalRead(digitalPin5);
  double error = (l3 * (-w3) + l2 * (-w2) + r2 * w2 + r3 * w3) / (l3 + l2 + m + r2 + r3);
  int powerCorrection = Kp * error;  // ex. Kp = 100, 也與w2 & w3有關
  int vR = Tp - powerCorrection;     // ex. Tp = 150, 也與w2 & w3有關
  int vL = Tp + powerCorrection;
  if (vR > 255) vR = 255;
  if (vL > 255) vL = 255;
  if (vR < -255) vR = -255;
  if (vL < -255) vL = -255;
  if (     (     (l2==1)  &&    (m==1)  &&     (r2==1)     )    ){     
    // delay(1000);
    MotorWriting(-100, 100);
    

  }
  else{
    MotorWriting(vL, vR);  //Feedback to motors
  }
}

void uturn();



void loop() {
  // put your main code here, to run repeatedly:
  // double vl = 30;
  // double vr = 30;
  double v=150;
  //digitalWrite(STBY, HIGH);
  Tracking(v);

  // MotorWriting(vl,vr);
}










