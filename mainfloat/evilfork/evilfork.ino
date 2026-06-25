#include "MS5837.h"
#include <SPI.h>
#include <Servo.h>
#include <Wire.h>
MS5837 sensor;
#define RYLR Serial1

byte holding = 0;   // how long the float has been maintaing depth
int dataIndex = 0; // current data point index
float depth = 0;
float output = 0;
char message;
int startTime = 0;
int startTimelog = 0;
bool SIM = false; // weather or not its in simualtion mode
float descentDepth = 1.1 + 1;
float Icesheet = 0.4 + 1;
// 0.46
float setpoint = descentDepth;

float surfaceDepth = 0; // the depth offset

Servo engine;

float fastTol = 0.20; // meters
float slowTol = 0.05; // meters
float fastMiSc = 315; // micro seconds
float slowMiSc = 50;

const byte datasizelenght = 180;

byte cdi = 0;

int times[datasizelenght];
int depths[datasizelenght];

void controller() {
    float error = setpoint - depth;

    if (fabs(error) <= slowTol) {
        // State 3: inside target window. Do not chase noise.
        output = 1327;
        Serial.println("HOLD_WINDOW");
    } else if (error > fastTol) {
        // State 1: VP is far above/shallower than target. Move down quickly.
        output = 1327 + fastMiSc;
        Serial.println("FAST_DEEPER");
    } else if (error > slowTol) {
        // State 2: VP is just above/shallower than target. Move down gently.
        output = 1327 + slowMiSc;
        Serial.println("SLOW_DEEPER");
    } else if (error < -fastTol) {
        // State 5: VP is far below/deeper than target. Move up quickly.
        output = 1327 - fastMiSc;
        Serial.println("FAST_SHALLOWER");
    } else {
        // State 4: VP is just below/deeper than target. Move up gently.
        output = 1327 - slowMiSc;
        Serial.println("SLOW_SHALLOWER");
    }
}

void sendradiomessage(String msg) {
    RYLR.print("AT+SEND=");
    RYLR.print("82");
    RYLR.print(",");
    RYLR.print(msg.length());
    RYLR.print(",");
    RYLR.print(msg);
    RYLR.print("\r\n");
}
void relay() {
    int lineindex = 0;
    char message;

    while (true) {
        updateDepth();
        controller();
        
        engine.writeMicroseconds(int(output));
        if (RYLR.available() > 0) {
            String line = RYLR.readStringUntil('\n');
            if (line[1] == 82 && line[2] == 67) {
                message = line[10];
            }
            line = "";
        }
        if (message == 'U') { // This means the float has been recovered and
                              // should upload data
            message = 'o';
            engine.write(0);
            break;
        }
    }
    for (int i = 0; i <= datasizelenght; i++) {
        String dataLine = "T"+String(times[i])+"TP"+String(float(depths[i])/10)+"PN"+String(i)+"N";
        // T int TPP flt PN int N
        sendradiomessage(dataLine);

        // wait for the topside to acknowledge
        while (message != 'n' or dataLine == "stop") {
            if (RYLR.available() > 0) {
                String line = RYLR.readStringUntil('\n');
                Serial.println(line);
                if (line[1] == 82 && line[2] == 67) {
                    Serial.print("message:");
                    message = line[10];
                    Serial.println(message);
                }
            }
            dataLine = "";
            if (message == 'r') {
                sendradiomessage(dataLine);
                message = 'o';
            }
        }
        message = 'o';
    }
    sendradiomessage("stop");
}
void updateDepth() {
    if (SIM) {
        if (Serial.available() > 0) {
            String line = Serial.readStringUntil('\n');
            if (line.length() > 0) {
                depth = line.toFloat();
            }
        }
    } else {
        sensor.read();
        // see caluclations
        // https://docs.google.com/spreadsheets/d/1Wab4LbDww71lHrJmSqJ-hdIlBZDHO0Bx2nWjerMkGF4/edit?usp=sharing

        float extra = 1;
        // idr why is its even like that
        // i remembered
        // our depth sensor spits out wrong depth values but they are roughly
        // linear with the real ones. the math stuff is to convert that to
        // normal
        depth = max(0, (((-104 * ((sensor.depth() * -1)) + 45.1) / 100) -
                        surfaceDepth)) +
                extra;
    }
}

void wait() {
    engine.writeMicroseconds(1000);
    Serial.println("WATING");
    while (true) {

        if (RYLR.available() > 0) {
            String line = RYLR.readStringUntil('\n');
            if (line[1] == 82 && line[2] == 67) {
                message = line[10];
            }
            Serial.println(line);
            line = "";
        }
        // Serial.println(message);
        if (message == 'H') {
            message = 'o';
            engine.writeMicroseconds(1000);
            RYLR.print("AT+SEND=82,2,hi");
            RYLR.print("\r\n");
            updateDepth();
            controller();
            startTime = millis();
            surfaceDepth = depth;
        }
        if (message == 'D') {
            message = 'o';
            RYLR.print("AT+SEND=82,2,good buoy");
            RYLR.print("\r\n");
            break;
        }
    }
}

void log() {
    times[cdi] = int((millis() - startTime) / 1000);
    depths[cdi] = int(depth * 10);
    cdi += 1;
}

void descend() {
    setpoint = descentDepth;
    startTimelog = millis();
    holding = 0;
    while (true) {

        updateDepth();
        controller();

        // send a debug message
        sendradiomessage(String(depth) + " : " + String(output) +
                         " ERROR: " + String(abs(descentDepth - depth)) + "," +
                         String(setpoint) + "HOLDE:" + String(holding));
        if (SIM) {
            Serial.print("D");
            Serial.println(output);
        } else {

            engine.writeMicroseconds(int(output));
        }

        if (millis() - startTimelog >= 5000) {
            startTimelog = millis();
            log();

            if (abs(descentDepth - depth) < 0.33) {
                holding++;
            } else {
                holding = 0;
            }

            if (holding > 5) {
                break;
            }
        }
        if (RYLR.available() > 0) {
            String line = RYLR.readStringUntil('\n');
            if (line[1] == 82 && line[2] == 67) {
                message = line[10];
            }
            Serial.println(line);
            line = "";
        }
        if (message == 'E') { // emergancy stop
            message = 'o';
            engine.writeMicroseconds(1000);
            while (true) {
                delay(10);
            }
        }
    }
}

void ascend() {
    setpoint = Icesheet;

    holding = 0;
    while (true) {

        startTimelog = millis();

        updateDepth();

        controller();

        // send a debug message
        sendradiomessage(String(depth) + " : " + String(output) +
                         " ERROR: " + String(abs(descentDepth - depth)) + "," +
                         String(setpoint) + "HOLDE:" + String(holding));
        if (SIM) {
            Serial.print("D");
            Serial.println(output);
        } else {
            engine.writeMicroseconds(int(output));
        }

        if (millis() - startTimelog >= 5000) {
            startTimelog = millis();
            log();
            // Serial.println(holding);
            if (abs(Icesheet - depth) < 0.33) {
                holding++;
            } else {
                holding = 0;
            }
            // holding = 0;
            if (holding > 7) {
                break;
            }
        }
        if (RYLR.available() > 0) {
            String line = RYLR.readStringUntil('\n');
            if (line[1] == 82 && line[2] == 67) {
                message = line[10];
            }
            Serial.println(line);
            line = "";
        }
        if (message == 'E') { // emergency stop
            message = 'o';
            engine.writeMicroseconds(1000);
            while (true) {
                delay(10);
            }
        }
    }
}

void setup() {

    Serial.begin(115200);
    RYLR.begin(115200);
    Serial.println("HI GUYS");
    for (int i = 0; i <= datasizelenght; i++) {
        depths[i] = 51;
        times[i] = 301;
    }

    // depths[0] = 10;
    // depths[1] = 20;
    // times[0] = 10;
    // times[1] = 20;

    // for (int i = 0; i <= datasizelenght; i++) {
    //     if (depths[i] < 50 and times[i] < 300) {
    //         Serial.println(depths[i]);
    //         Serial.println(times[i]);
    //     }
    // }

    while (!Serial && millis() < 4000)
        ; // Wait up to 4s for Serial Monitor
    Serial.println("--- STARTING SETUP ---");
    while (!RYLR) {
        Serial.println("D:");
    }
    if (!SIM) {
        engine.attach(9);
    }
    Serial.println("conneted");
    RYLR.print("AT\r\n");
    Serial.println("Sent 'AT\\r\\n' command. Waiting for response...");

    if (!SIM) {
        Wire.begin();
        sensor.setModel(MS5837::MS5837_02BA);
        while (!sensor.init()) {
            Serial.println("Init failed!");
            Serial.println("Are SDA/SCL connected correctly?");
            Serial.println("Blue Robotics Bar30: White=SDA, Green=SCL");
            Serial.println("\n\n\n");
            delay(500);
        }
        sensor.setFluidDensity(997);
    }
    delay(1000);
    Serial.setTimeout(10);
}

void loop() {
    // colours

    if (!SIM) {
        wait();
    }

    descend();

    ascend();

    descend();

    ascend();

    relay();

    while (true) {
    }
}