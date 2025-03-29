/***************************************************************************/
// File			  [track.h]
// Author		  [Erik Kuo]
// Synopsis		[Code used for tracking]
// Functions  [MotorWriting, MotorInverter, tracking]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 1 & 6*/
/*feel free to add your own function for convenience*/

/*===========================import variable===========================*/
int extern TP;
/*===========================import variable===========================*/

// Write the voltage to motor.
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
}  // MotorWriting

// Handle negative motor_PWMR value.
void MotorInverter(int motor, bool& dir) {
    // Hint: the value of motor_PWMR must between 0~255, cannot write negative value.
}  // MotorInverter

// P/PID control Tracking


// void Tracking(double v) {
//   int w2 = 1.1;
//   int w3 = 1.2;
//   int Tp = v;
//   int Kp = Tp * 0.5;
//   int l3 = digitalRead(digitalPin1);
//   int l2 = digitalRead(digitalPin2);
//   int m = digitalRead(digitalPin3);
//   int r2 = digitalRead(digitalPin4);
//   int r3 = digitalRead(digitalPin5);

  
//     while(l2!=0 && r2!=0){
//       MotorWriting(80,80);
//       l2 = digitalRead(digitalPin2);
//       r2 = digitalRead(digitalPin4);
//     }


//   } else {
//     double error = (l3 * (-w3) + l2 * (-w2) + r2 * w2 + r3 * w3) / (l3 + l2 + m + r2 + r3);
//     double denominator = (l3 + l2 + m + r2 + r3);
//     if (denominator == 0) {
//       error = 0;  // 若所有感測器皆未觸發，則 error 設為 0
//     } else {
//       error = (l3 * (-w3) + l2 * (-w2) + r2 * w2 + r3 * w3) ;
//     }
//     int powerCorrection = Kp * error;  // ex. Kp = 100, 也與w2 & w3有關
//     int vR = Tp - powerCorrection;     // ex. Tp = 150, 也與w2 & w3有關
//     int vL = Tp + powerCorrection;
//     if (vR > 255) vR = 255;
//     if (vL > 255) vL = 255;
//     if (vR < -255) vR = -255;
//     if (vL < -255) vL = -255;
//     MotorWriting(vL, vR);  //Feedback to motors
//   }
// }


