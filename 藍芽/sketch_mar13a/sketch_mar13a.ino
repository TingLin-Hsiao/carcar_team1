#include <SoftwareSerial.h>

// 定義 SoftwareSerial 物件，指定 RX = 10, TX = 11
SoftwareSerial BT(10,11);

void setup() {
  Serial.begin(9600);  // 開啟 Serial Monitor
  BT.begin(9600);      // 開啟藍牙通訊
}

void loop() {
  // 如果藍牙有資料傳入，讀取並傳到 Serial Monitor
  if (BT.available()) {
    char c = BT.read();
    Serial.print(c);
  }

  // 如果 Serial Monitor 有輸入，傳送到藍牙模組
  if (Serial.available()) {
    char c = Serial.read();
    BT.print(c);
  }
  delay(100);
}
