/***************************************************************************/
// File			  [bluetooth.h]
// Author		  [Erik Kuo]
// Synopsis		[Code for bluetooth communication]
// Functions  [ask_BT, send_msg, send_byte]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 2*/
#include<SoftwareSerial.h>
extern SoftwareSerial BT;

enum BT_CMD {
    NOTHING = 0,
    FORWARD = 1,
    BACKWARD = 2,
    LEFT = 3,
    RIGHT = 4,
    STOP = 5
    // TODO: add your own command type here
};

BT_CMD ask_BT() {
    BT_CMD message = NOTHING;
    char cmd;
    if (BT.available()) {
        cmd = BT.read();
        if(cmd) Serial.println(cmd);
        delay(100);
    
    
// TODO:    
// 1. get cmd from BT(bluetooth serial)
// 2. link bluetooth message to your own command type

#ifdef DEBUG
        //Serial.print("cmd : ");
        //Serial.println(cmd);
#endif
        switch (cmd) {
            case 'F': message = FORWARD; break;
            case 'B': message = BACKWARD; break;
            case 'L': message = LEFT; break;
            case 'R': message = RIGHT; break;
            case 'S': message = STOP; break;
            default: message = NOTHING; break;
        }
    }
    
    
    return message;
}  // ask_BT


// send msg back through BT(bluetooth serial)
// can use send_byte alternatively to send msg back
// (but need to convert to byte type)
void send_msg(const char& msg) {
    // TODO:
    BT.print(msg);
// #ifdef DEBUG
//     Serial.print("Sent message: ");
//     Serial.println(msg);
// #endif
}  // send_msg

// send UID back through BT(bluetooth serial)
void send_byte(byte* id, byte& idSize) {
  if (id == nullptr || idSize == 0) {  // Check for invalid UID
        Serial.println("Error: No valid UID detected!");
        BT.print("Error: No valid UID");
        return;
    }
  for (byte i = 0; i < idSize; i++) {  // Send UID consequently.
    if (id[i]<16){
      // BT.write(byte(0));
      BT.write(id[i]);
    }
    else{
      BT.write(id[i]);
    }
  }
#ifdef DEBUG
    Serial.print("Sent id: ");
    for (byte i = 0; i < idSize; i++) {  // Show UID consequently.
        if (id[i]<16){
          Serial.print("0");
        }
        Serial.print(id[i], HEX);
    }
    Serial.println();
#endif
}  // send_byte
