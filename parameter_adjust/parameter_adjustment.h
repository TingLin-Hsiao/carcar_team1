#include "pin_define.h"
#include "track.h"




void Forward(double v){
    MotorWriting(v, v);
    delay(380);
}

void Backward(double v){
    MotorWriting(-v, v);
    delay(830);
}

void Left(double v){
    MotorWriting(-v, v);
    delay(380);
}

void Right(double v){
    MotorWriting(v, -v);
    delay(380);
}

void Stop(double v){
    MotorWriting(0, 0);
}
           