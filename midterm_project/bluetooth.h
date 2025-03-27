/***************************************************************************/
// File			  [bluetooth.h]
// Author		  [Erik Kuo]
// Synopsis		[Code for bluetooth communication]
// Functions  [ask_BT, send_msg, send_byte]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 2*/

enum BT_CMD {
    NOTHING,
    FORWARD,
    BACKWARD,
    LEFT,
    RIGHT,
    STOP
    // TODO: add your own command type here
};

BT_CMD ask_BT() {
    BT_CMD message = NOTHING;
    char cmd;
    if (Serial1.available()) {
        cmd = Serial1.read();
        // Serial.print(cmd);
// TODO:
// 1. get cmd from BT(bluetooth serial)
// 2. link bluetooth message to your own command type
#ifdef DEBUG
        Serial.print("cmd : ");
        Serial.println(cmd);
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
    Serial1.print(msg);
#ifdef DEBUG
    Serial.print("Sent message: ");
    Serial.println(msg);
#endif
}  // send_msg

// send UID back through BT(bluetooth serial)
void send_byte(byte* id, byte& idSize) {
    for (byte i = 0; i < idSize; i++) {  // Send UID consequently.
      Serial1.write(id[i]);
    }
#ifdef DEBUG
    Serial.print("Sent id: ");
    for (byte i = 0; i < idSize; i++) {  // Show UID consequently.
        Serial.print(id[i], HEX);
    }
    Serial.println();
#endif
}  // send_byte
