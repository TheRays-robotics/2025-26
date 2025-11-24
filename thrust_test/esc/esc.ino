#include <Servo.h>
Servo esc;
void setup() {
  // put your setup code here, to run once:
esc.attach(9);
esc.writeMicroseconds(20000);


}

void loop() {
  // put your main code here, to run repeatedly:

esc.writeMicroseconds(2000);

}