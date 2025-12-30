#include <Servo.h>
Servo esc;
void setup() {
  // put your setup code here, to run once:
esc.attach(9);
esc.write(0);
for (int i = 1; i <= 180; i++) {
delay(100);
esc.write(i);
}


}

void loop() {
  // put your main code here, to run repeatedly:


}