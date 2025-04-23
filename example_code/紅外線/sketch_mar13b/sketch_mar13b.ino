#define ledPin 13
#define digitalPin1 32 //前置命令定義 analogPin 來自於 A0
#define digitalPin2 34
#define digitalPin3 36
#define digitalPin4 38
#define digitalPin5 40


void setup() {
 pinMode(digitalPin1 , INPUT); // 目前預設該接腳作為輸入
  pinMode(digitalPin2 , INPUT);
   pinMode(digitalPin3 , INPUT);
    pinMode(digitalPin4 , INPUT);
     pinMode(digitalPin5 , INPUT);

 Serial.begin(9600); // 表示開始傳遞與接收序列埠資料
}
void loop(){

 int sensorValue2 = digitalRead(digitalPin1);
 int sensorValue1 = digitalRead(digitalPin2);
 int sensorValue3 = digitalRead(digitalPin3);
 int sensorValue4 = digitalRead(digitalPin4);
 int sensorValue5 = digitalRead(digitalPin5);
// 宣告 sensorValue 這變數是整數(Integer)
 Serial.println(sensorValue2); // 將數值印出來

 if(sensorValue2==0){
  Serial.println("2white");
 }
 else{
  Serial.println("2black");
 }
 if(sensorValue1==0){
  Serial.println("1white");
 }
 else{
  Serial.println("1black");
 }
  if(sensorValue3==0){
  Serial.println("3white");
 }
 else{
  Serial.println("3black");
 }
  if(sensorValue4==0){
  Serial.println("4white");
 }
 else{
  Serial.println("4black");
 }
  if(sensorValue5==0){
  Serial.println("5white");
 }
 else{
  Serial.println("5black");
 }
 
 delay (1000); // 延遲 0.5 秒
}































