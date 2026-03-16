#include "ArduPID.h"
#include <SD.h>
#include <SPI.h>

#include <DS1307RTC.h>
#include <TimeLib.h>
#include <Wire.h>
const int chipSelect = BUILTIN_SDCARD;

#define RYLR Serial2
TeensyPID pid;
int holding = 0;
int dataIndex = 0;
float setpoint = 2.5f;
float depth = 0.0f;
float output = 0.0f;
char message;

IntervalTimer controlTimer;

void controlLoop() { output = pid.compute(setpoint, depth); }

void wait() {
    while (true) {
        // Serial.println("D0");
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
        if (message == 'D') {
            message = 'o';
            RYLR.print("AT+SEND=82,1");
            RYLR.println(message);
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
    setpoint = 2.5;
    holding = 0;
    while (true) {
        static elapsedMillis timer;
        static elapsedMillis datalogclock;
        

        if (Serial.available() > 0) {
            String line = Serial.readStringUntil('\n');
            if (line.length() > 0) {
                depth = line.toFloat();
            }
        }

        if (timer > 200) {
            timer = 0;
            Serial.print("D");
            Serial.println(output);
        }

        if (datalogclock >= 5000) {
            datalogclock = 0;
            log();
            Serial.println(holding);
            if (abs(2.5 - depth) < 0.5) {
                holding++;
            }
            else{
                holding = 0;
            }
            if (holding > 5){
                break;
            }

        }
    }
}

void ascend() {
    setpoint = 0.2;
    holding = 0;
    while (true) {
        static elapsedMillis timer;
        static elapsedMillis datalogclock;

        if (Serial.available() > 0) {
            String line = Serial.readStringUntil('\n');
            if (line.length() > 0) {
                depth = line.toFloat();
            }
        }

        if (timer > 200) {
            timer = 0;
            Serial.print("D");
            Serial.println(output);
        }

        if (datalogclock >= 5000) {
            datalogclock = 0;
            log();
            Serial.println(holding);
            if (abs(0.4 - depth) < 0.33) {
                holding++;
            }
            else{
                holding = 0;
            }
            if (holding > 5){
                break;
            }

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
    setSyncProvider(RTC.get); // the function to get the time from the RTC
    if (timeStatus() != timeSet)
        Serial.println("Unable to sync with the RTC");
    else
        Serial.println("RTC has set the system time");
}
void relay(){
int lineindex = 0;
char message;

Serial.println("yippee");
File myFile = SD.open("data.txt");
Serial.println("yippee1");
//if (myFile) {
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
    RYLR.print("\r\n");  // Critical: Module requires both \r and \n

    // Print to Serial Monitor for debugging
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