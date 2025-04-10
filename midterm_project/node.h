/***************************************************************************/
// File			  [node.h]
// Author		  [Erik Kuo, Joshua Lin]
// Synopsis		[Code for managing car movement when encounter a node]
// Functions  [/* add on your own! */]
// Modify		  [2020/03/027 Erik Kuo]
/***************************************************************************/

/*===========================import variable===========================*/
int extern _Tp;
#include"pin_define.h"
#include"queue.h"
// #include "track.h"
/*===========================import variable===========================*/

// TODO: add some function to control your car when encounter a node
// here are something you can try: left_turn, right_turn... etc.

bool IsNode(){
    int l3 = digitalRead(digitalPin1);
    int l2 = digitalRead(digitalPin2);
    int m  = digitalRead(digitalPin3);
    int r2 = digitalRead(digitalPin4);
    int r3 = digitalRead(digitalPin5);
    return l2 && m && r2;
}
