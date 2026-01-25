#include "ArduPID.h"




ArduPID myController;




double input;
double output;

// Arbitrary setpoint and gains - adjust these as fit for your project:
double setpoint = 2.5;
double p = 0;
double i = 0;
double d = 0;
double b = 0;



void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(A0));
  p = random(0, 100);
  i = 0;
  d = 0;
  myController.begin(&input, &output, &setpoint, p, i, d);

  //myController.reverse();               // Uncomment if controller output is "reversed"
  //myController.setSampleTime(10);      // OPTIONAL - will ensure at least 10ms have past between successful compute() calls
  myController.setOutputLimits(0, 180);
  myController.setBias(90);
  myController.setWindUpLimits(-10, 10);  // Groth bounds for the integral term to prevent integral wind-up

  myController.start();
  // myController.reset();               // Used for resetting the I and D terms - only use this if you know what you're doing
  // myController.stop();                // Turn off the PID controller (compute() will not do anything until start() is called)
}




void loop() {
  if (Serial.available() > 0) {
    //weight = random(-1000,1000);
    String line = Serial.readStringUntil('\n', 1000);
    Serial.println("line");
    //Serial.println(line);
    if (line != "") {
      input = line.toFloat();
    }
  }  // Replace with sensor feedback
  Serial.print("P");
  Serial.print(p);
  Serial.print(",");
  Serial.print(d);
  Serial.print(",");
  Serial.print(i);
  Serial.print(",");
  Serial.println(b);
  myController.compute();
  // myController.debug(&Serial, "myController", PRINT_INPUT |     // Can include or comment out any of these terms to print
  //                                               PRINT_OUTPUT |  // in the Serial plotter
  //                                               PRINT_SETPOINT | PRINT_BIAS | PRINT_P | PRINT_I | PRINT_D);
  Serial.print("M");
  Serial.println(output);  // Replace with plant control signal
  delay(10);
  //}
  //}
}