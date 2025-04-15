/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

#define DEBUG  // debug flag

// for RFID
#include <MFRC522.h>
#include <SPI.h>
using namespace std;

/*===========================define pin & create module object================================*/
// BlueTooth
// BT connect to BT (Hardware Serial)
// Mega               HC05
// Pin  (Function)    Pin
// 18    TX       ->  RX
// 19    RX       <-  TX
// TB6612, 請按照自己車上的接線寫入腳位(左右不一定要跟註解寫的一樣)
// TODO: 請將腳位寫入下方
#define AIN1 2     // 定義 A1 接腳（右）
#define AIN2 3     // 定義 A2 接腳（右）
#define PWMA 13  // 定義 ENA (PWM調速) 接腳
#define BIN1 5     // 定義 B1 接腳（左）
#define BIN2 6     // 定義 B2 接腳（左）
#define PWMB 12  // 定義 ENB (PWM調速) 接腳
// 循線模組, 請按照自己車上的接線寫入腳位
#define digitalPin1 32
#define digitalPin2 34
#define digitalPin3 36
#define digitalPin4 38
#define digitalPin5 40
// RFID, 請按照自己車上的接線寫入腳位
#define RST_PIN 9                 // 讀卡機的重置腳位
#define SS_PIN 53                  // 晶片選擇腳位
MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件

#include<SoftwareSerial.h>
/*===========================define pin & create module object===========================*/
SoftwareSerial BT(10,11);
/*============setup============*/
void setup() {
    // bluetooth initialization
    BT.begin(9600);
    // Serial window
    Serial.begin(9600);
    // RFID initial
    SPI.begin();
    mfrc522.PCD_Init();
    // TB6612 pin
    pinMode(AIN1, OUTPUT);
    pinMode(AIN2, OUTPUT);
    pinMode(BIN1, OUTPUT);
    pinMode(BIN2, OUTPUT);
    pinMode(PWMB, OUTPUT);
    pinMode(PWMA, OUTPUT);
    // tracking pin
    pinMode(digitalPin1, INPUT);
    pinMode(digitalPin2, INPUT);
    pinMode(digitalPin3, INPUT);
    pinMode(digitalPin4, INPUT);
    pinMode(digitalPin5, INPUT);
#ifdef DEBUG
    Serial.println("Start!");
#endif
}
/*============setup============*/

/*=====Import header files=====*/
#include "pin_define.h"
#include "RFID.h"
#include "node.h"
#include "track.h"
#include "bluetooth.h"
#include "queue.h"

/*=====Import header files=====*/

/*===========================initialize variables===========================*/
//int l2 = 0, l1 = 0, m0 = 0, r1 = 0, r2 = 0;  // 紅外線模組的讀值(0->white,1->black)
int v = 200;       
//int yee=0;                         // set your own value for motor power
bool state = false;     // set state to false to halt the car, set state to true to activate the car
bool state2 = false;
BT_CMD _cmd = NOTHING;  // enum for bluetooth message, reference in bluetooth.h line 2
Queue<BT_CMD,100> commandQueue;
int Fdelay=300;
int Bdelay=300;
int Ldelay=300;
int Rdelay=300;
// double w1=300;
// double w2=;
// double Kp=

/*===========================initialize variables===========================*/

/*===========================declare function prototypes===========================*/
void Search();    // search graph
void SetState();  // switch the state
void CheckRFID();      // 
void NextAction(double v);
/*===========================declare function prototypes===========================*/

/*===========================define function===========================*/
void loop() {
    if (!state)
        MotorWriting(0, 0);
    else
        Search();
    SetState();

    CheckRFID();
    //Serial.println(yee++);
    //delay(50);  // Small delay to avoid excessive CPU usage
}


void SetState() {
    _cmd = ask_BT();
    if (_cmd!=NOTHING){
      state=true;
      commandQueue.enqueue(_cmd);
    
    int delay;
    delay=ask_delay();
    Serial.println(delay);
    commandQueue.enqueue(STOP);
    if(_cmd==RIGHT) Rdelay=delay;
    if(_cmd==LEFT) Ldelay=delay;
    if(_cmd==FORWARD) Fdelay=delay;
    if(_cmd==BACKWARD) Bdelay=delay;
    }
}

void Search() {
    // TODO: let your car search graph(maze) according to bluetooth command from computer(python
    // code)
    // tracking(l2,l1,m,r1,r2);
  int Tp = v;
  int Kp = Tp * 0.5;
  int l3 = digitalRead(digitalPin1);
  int l2 = digitalRead(digitalPin2);
  int m = digitalRead(digitalPin3);
  int r2 = digitalRead(digitalPin4);
  int r3 = digitalRead(digitalPin5);

  if (l2 && m && r2) {
    while(l2!=0 && r2!=0){
      CheckRFID();
      MotorWriting(v*0.6,v*0.6);
      l2 = digitalRead(digitalPin2);
      r2 = digitalRead(digitalPin4);
    }
    NextAction(v);
  } else {
    Tracking(v);
  }

}


void CheckRFID(){
  byte idSize;
  byte* uid = rfid(idSize);  // Call rfid() to check for a card

  if (uid) {  // If an RFID card is detected
      send_byte(uid,idSize);
      delay(100);
  }

}

void NextAction(double v){
  BT_CMD cmd = commandQueue.peek();
  Serial.println(cmd);
  switch (cmd) {
      case FORWARD:
          //state = true;
          MotorWriting(v, v);
          delay(Fdelay);
          break;
      case BACKWARD:
          //state = true;
          MotorWriting(-v, v);
          delay(Bdelay);
          break;
      case LEFT:
          //state = true;
          MotorWriting(-v, v);
          delay(Ldelay);
          break;
      case RIGHT:
          //state = true;
          MotorWriting(v, -v);
          delay(Rdelay);
          break;
      case STOP:
          state = false;
          MotorWriting(0, 0);
          break;
      default:
          break;
    
  }
  commandQueue.dequeue();
}
/*===========================define function===========================*/
