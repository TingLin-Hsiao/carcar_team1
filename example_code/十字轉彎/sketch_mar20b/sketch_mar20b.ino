int PWMA = 13;
int PWMB = 12;
int AIN2 = 3;
int AIN1 = 2;
int BIN1 = 5;
int BIN2 = 6;
//int STBY = 5;


#define ledPin 13
#define digitalPin1 32  //前置命令定義 analogPin 來自於 A0
#define digitalPin2 34
#define digitalPin3 36
#define digitalPin4 38
#define digitalPin5 40
int do_list[6]={2,1,3,1,0,4};
int i=0;



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
  vR = vR * 0.93;
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


void turn(int t){
  if(t==0){
    //leftturn
    MotorWriting(-80,80);
    delay(450);
  }
  else if(t==1){
    //uturn
    MotorWriting(-80,80);
    delay(900);
  }
  else if(t==2){
    //righturn
    MotorWriting(80,-80);
    delay(450);
  }
  else if(t==3){
    MotorWriting(80,80);
    delay(450);
  }
  else if(t>=4){
    MotorWriting(0,0);
    delay(10000);
  }
}


void Tracking(double v) {
  int w2 = 1.1;
  int w3 = 1.2;
  int Tp = v;
  int Kp = Tp * 0.5;
  int l3 = digitalRead(digitalPin1);
  int l2 = digitalRead(digitalPin2);
  int m = digitalRead(digitalPin3);
  int r2 = digitalRead(digitalPin4);
  int r3 = digitalRead(digitalPin5);

  if (l2 && m && r2) {
    while(l2!=0 && r2!=0){
      MotorWriting(80,80);
      l2 = digitalRead(digitalPin2);
      r2 = digitalRead(digitalPin4);
    }

    turn(do_list[i]);
    i+=1;
  } else {
    double error = (l3 * (-w3) + l2 * (-w2) + r2 * w2 + r3 * w3) / (l3 + l2 + m + r2 + r3);
    double denominator = (l3 + l2 + m + r2 + r3);
    if (denominator == 0) {
      error = 0;  // 若所有感測器皆未觸發，則 error 設為 0
    } else {
      error = (l3 * (-w3) + l2 * (-w2) + r2 * w2 + r3 * w3) ;
    }
    int powerCorrection = Kp * error;  // ex. Kp = 100, 也與w2 & w3有關
    int vR = Tp - powerCorrection;     // ex. Tp = 150, 也與w2 & w3有關
    int vL = Tp + powerCorrection;
    if (vR > 255) vR = 255;
    if (vL > 255) vL = 255;
    if (vR < -255) vR = -255;
    if (vL < -255) vL = -255;
    MotorWriting(vL, vR);  //Feedback to motors
  }
}

//void uturn();



void loop() {
  // put your main code here, to run repeatedly:
  // double vl = 30;
  // double vr = 30;
  
  double v = 80;
  //digitalWrite(STBY, HIGH);
  Tracking(v);

  // MotorWriting(150,150);
}
