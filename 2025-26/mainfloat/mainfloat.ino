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
TeensyPID pid;

int holding = 0;
int dataIndex = 0;
float setpoint = 2.5f;
float depth = 0.0f;
float output = 0.0f;
char message;

bool SIM = false;
float descentDepth = 0.25;
float surfaceDepth = 0;

Servo engine;
IntervalTimer controlTimer;

void controlLoop() { output = pid.compute(setpoint, depth); }

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

        depth =
            max(0,(((-104 * ((sensor.depth() * -1)) + 45.1) / 100) - surfaceDepth));
    }
}

void wait() {
    engine.writeMicroseconds(1000);
    while (true) {

        if (RYLR.available() > 0) {
            String line = RYLR.readStringUntil(10, 1000);
            if (line[1] == 82 && line[2] == 67) {
                message = line[10];
            }
            Serial.println(line);
            for (int i = 0; i < sizeof(line); ++i) {
                line[i] = 0;
            }
        }
        // Serial.println(message);
        if (message == 'H') {
            message = 'o';
            engine.writeMicroseconds(1000);
            RYLR.print("AT+SEND=82,2,hi");
            RYLR.print("\r\n");
            updateDepth();
            surfaceDepth = depth;
        }
        if (message == 'D') {
            message = 'o';
            // RYLR.print("AT+SEND=82,2,hi");
            // RYLR.print("\r\n");
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
    holding = 0;
    while (true) {

        static elapsedMillis timer;
        static elapsedMillis datalogclock;

        updateDepth();

        if (timer > 200) {
            timer = 0;
            if (SIM) {
                Serial.print("D");
                Serial.println(output);
            } else {
                output = map(output, 0, 180, 0, 100);
                engine.write(output);
                // engine.write(100);
                Serial.print("D");
                Serial.println(output);

                String dataLine = String(depth)+" : "+String(output);
                RYLR.print("AT+SEND=");
                RYLR.print("82");
                RYLR.print(",");
                RYLR.print(dataLine.length());
                RYLR.print(",");
                RYLR.print(dataLine);
                RYLR.print("\r\n");
            }
        }

        if (datalogclock >= 5000) {
            datalogclock = 0;
            log();
            // Serial.println(holding);
            if (abs(2.5 - depth) < 0.5) {
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
            for (int i = 0; i < sizeof(line); ++i) {
                line[i] = 0;
            }
        }
        if (message == 'E') {
            message = 'o';
            engine.write(0);
            while (true){
                delay(10);
            }
        }
    }
}

void ascend() {
    setpoint = 0.4;
    holding = 0;
    while (true) {
        static elapsedMillis timer;
        static elapsedMillis datalogclock;

        updateDepth();

        if (timer > 200) {
            timer = 0;
            if (SIM) {
                Serial.print("D");
                Serial.println(output);
            } else {
                output = map(output, 0, 180, 0, 100);
                engine.write(output);
            }
        }

        if (datalogclock >= 5000) {
            datalogclock = 0;
            log();
            Serial.println(holding);
            if (abs(0.4 - depth) < 0.33) {
                holding++;
            } else {
                holding = 0;
            }
            if (holding > 5) {
                break;
            }
        }
    }
}

void setup() {

    Serial.begin(115200);
    RYLR.begin(115200);
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

    pid.begin(1000.0f, 800.0f, 5.0f, 0.001f, 0.0f, 180.0f, TeensyPID::P_ON_E,
              TeensyPID::D_ON_M, TeensyPID::FORWARD, 0.0f);

    pid.setWindupLimits(0.0f, 180.0f);
    controlTimer.begin(controlLoop, 1000);
    setSyncProvider(RTC.get);
    if (timeStatus() != timeSet)
        Serial.println("Unable to sync with the RTC");
    else
        Serial.println("RTC has set the system time");
}
void relay() {
    int lineindex = 0;
    char message;

    Serial.println("yippee");
    File myFile = SD.open("data.txt");
    Serial.println("yippee1");

    Serial.println("Reading data.txt:");
    while (myFile.available()) {
        String dataLine = myFile.readStringUntil(10, 1000);

        dataLine.trim();

        RYLR.print("AT+SEND=");
        RYLR.print("82");
        RYLR.print(",");
        RYLR.print(dataLine.length());
        RYLR.print(",");
        RYLR.print(dataLine);
        RYLR.print("\r\n");

        Serial.print("Command Sent: AT+SEND=");
        Serial.print("82");
        Serial.print(",");
        Serial.print(dataLine.length());
        Serial.print(",");
        Serial.println(dataLine);
        delay(0);
        for (int i = 0; i < sizeof(dataLine); ++i) {
            dataLine[i] = 0;
        }
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
        }
        message = 'o';
    }
}

void loop() {

    wait();
    Serial.println("descendeing");
    descend();
    Serial.println("ascending");
    ascend();
    relay();
}