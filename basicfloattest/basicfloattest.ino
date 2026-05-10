#include <Servo.h>
Servo engine;
#define lights Serial1

void setup() {
    // put your setup code here, to run once:
    lights.begin(9600);
    engine.attach(9);
    engine.writeMicroseconds(1655);
    delay(1000*2);
    engine.writeMicroseconds(1000);
    delay(1000*2);
}

void loop() {
    engine.writeMicroseconds(1655);
    lights.print("m");
    delay(1000*15);
    engine.writeMicroseconds(1000);
    lights.print("c");
    delay(1000*15);

    
}
