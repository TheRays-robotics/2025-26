#include "ArduPID.h"

#define RYLR Serial2
TeensyPID pid;

float setpoint = 2.5f;
float input = 0.0f;
float output = 0.0f;

IntervalTimer controlTimer;

void controlLoop() { output = pid.compute(setpoint, input); }

void wait() {
    while (true) {
        if (RYLR.available() > 0) {
            String line = RYLR.readStringUntil(10, 1000);
            if (line[1] == 82 && line[2] == 67) {
                message = line[10];
            }
            for (int i = 0; i < sizeof(line); ++i) {
                line[i] = 0;
            }
        }
        if (message == 'D') {
            message = 'o';
            break;
            }
    }
}

void setup() {
    Serial.begin(115200); // Faster baud rate recommended for Teensy
    RYLR.begin(115200);
    while (!RYLR) {
        Serial.println("D:");
    }
    Serial.println("conneted");
    RYLR.print("AT\r\n");
    Serial.println("Sent 'AT\\r\\n' command. Waiting for response...");

    delay(1000);

    pid.begin(1000.0f, // P - Proportional
              800.0f,  // I - Integral (helps reach exact setpoint)
              5.0f,    // D - Derivative (prevents bouncing)
              0.001f,
              0.0f,   // Min PID Output
              180.0f, // Max PID Output
              TeensyPID::P_ON_E, TeensyPID::D_ON_M, TeensyPID::FORWARD, 0.0f);

    pid.setWindupLimits(0.0f, 180.0f);
    controlTimer.begin(controlLoop, 1000);
}

void loop() {

    wait();

    static elapsedMillis timer;

    if (Serial.available() > 0) {
        String line = Serial.readStringUntil('\n');
        if (line.length() > 0) {
            input = line.toFloat();
        }
    }

    if (timer > 20) {
        timer = 0;
        Serial.println(output);
    }
}