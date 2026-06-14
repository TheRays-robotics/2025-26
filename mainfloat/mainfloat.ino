#include "ArduPID.h"
#include "MS5837.h"
#include <DS1307RTC.h>
#include <SD.h>
#include <SPI.h>
#include <Servo.h>
#include <TimeLib.h>
#include <Wire.h>
const int chipSelect = BUILTIN_SDCARD;
MS5837 sensor;
#define RYLR Serial2
#define lights Serial1
ArduPID pid;

int holding = 0;   // how long the float has been maintaing depth
int dataIndex = 0; // current data point index
float depth = 0.0f;
float output = 0.0f;
char message;

bool SIM = false; // weather or not its in simualtion mode
float descentDepth = 1;
float Icesheet = 0.4;
float setpoint = descentDepth;

float surfaceDepth = 0; // the depth offset

Servo engine;

double Kp = 720.0, Ki = 40.0, Kd = 0.0;

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

    File myFile = SD.open("data.txt"); // open the file
    while (true) {
        updateDepth();
        pid.compute(depth);
        output = pid.getSignals().out;
        engine.writeMicroseconds(int(output));
        if (RYLR.available() > 0) {
            String line = RYLR.readStringUntil(10, 1000);
            if (line[1] == 82 && line[2] == 67) {
                message = line[10];
            }
            line = "";
        }
        if (message == 'U') { // This means the float has been recovered and
                              // should upload data
            message = 'o';
            engine.write(0);
            lights.println("w");
            break;
        }
    }
    while (myFile.available()) {
        String dataLine = myFile.readStringUntil(10, 1000); // get just one line
        delay(500);
        dataLine.trim(); // remove any nonsense

        if (dataLine.length() > 0) {
            sendradiomessage(dataLine);
            Serial.println("Sent: " + dataLine);
        }

        // wait for the topside to acknowledge
        while (message != 'n' or dataLine == "stop") {
            if (RYLR.available() > 0) {
                String line = RYLR.readStringUntil(10, 1000);
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

        float extra = 0;
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
            String line = RYLR.readStringUntil(10, 1000);
            if (line[1] == 82 && line[2] == 67) {
                message = line[10];
            }
            Serial.println(line);
            line = "";
        }
        // Serial.println(message);
        if (message == 'H') {
            message = 'o';
            lights.print("r");
            engine.writeMicroseconds(1000);
            RYLR.print("AT+SEND=82,2,hi");
            RYLR.print("\r\n");
            updateDepth();
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

    File datafile = SD.open("data.txt", FILE_WRITE);
    datafile.print("T");
    datafile.print(second() + (minute() * 60));
    datafile.print("TP");
    datafile.print("P");
    datafile.print(depth);
    datafile.print("PN");
    datafile.print(dataIndex);
    datafile.println("N");
    datafile.close();
    dataIndex++;
}

void descend() {
    setpoint = descentDepth;
    pid.setSetpoint(setpoint);
    holding = 0;
    while (true) {

        static elapsedMillis datalogclock;

        updateDepth();
        pid.compute(depth);
        output = pid.getSignals().out;
        // send a debug message
        sendradiomessage(String(depth) + " : " + String(output) +
                         " ERROR: " + String(abs(descentDepth - depth)) + "," +
                         String(setpoint) + "HOLDE:" + String(holding));
        if (SIM) {
            Serial.print("D");
            Serial.println(output);
        } else {
            // move the syringe acourding to the PID controller
            engine.writeMicroseconds(int(output));
        }

        if (datalogclock >= 5000) {
            datalogclock = 0;
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
            String line = RYLR.readStringUntil(10, 1000);
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
    pid.compute(depth);
    pid.setSetpoint(setpoint);
    output = pid.getSignals().out;

    holding = 0;
    while (true) {

        static elapsedMillis datalogclock;

        updateDepth();
        pid.compute(depth);
        output = pid.getSignals().out;
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

        if (datalogclock >= 5000) {
            datalogclock = 0;
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
            String line = RYLR.readStringUntil(10, 1000);
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
    lights.begin(9600);
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
    if (!SD.begin(BUILTIN_SDCARD)) {
        Serial.println("SD Card Initialization Failed!");
        return;
    }
    SD.remove("data.txt");
    if (SD.exists("data.txt")) {
        Serial.print(F("Could not delete file"));
        Serial.println("data.txt");
    } else {
        Serial.println(F("All files deleted"));
    }
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
    pid.setSetpoint(setpoint);
    pid.setTunings(Kp, Ki, Kd);
    pid.setOutputLimits(1000.0f, 1655.0f);
    pid.setDirection((ArduPID::Direction)1);
    pid.setAntiWindMode((ArduPID::AntiWindMode)1);
    // pid.setWindUpLimits(-50.0f, 50.0f);
    // pid.setPMode(P_ON_E);
    // pid.setAntiWindMode(NONE);
    // pid.setDirection(0);
    setSyncProvider(RTC.get);
    if (timeStatus() != timeSet)
        Serial.println("Unable to sync with the RTC");
    else
        Serial.println("RTC has set the system time");
}

void loop() {
    // the lights take single charectors over serial corrisponding to predefined
    // colours

    if (!SIM) {
        lights.print("R");
        wait();
    }

    lights.println("y");
    descend();

    lights.println("g");
    ascend();

    lights.println("c");
    descend();

    lights.println("b");
    ascend();

    lights.println("m");
    relay();

    lights.println("w");
    while (true) {
    }
}