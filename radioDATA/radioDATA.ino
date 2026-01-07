#define RYLR Serial2
#include <SD.h>
#include <SPI.h>
const int chipSelect = BUILTIN_SDCARD;

void setup() {

  // put your setup code here, to run once:

  Serial.begin(115200);
  // Initialize the second serial port for communication with another device
  RYLR.begin(115200);
  if (!SD.begin(BUILTIN_SDCARD)) {
    Serial.println("SD Card Initialization Failed!");
    return;
  }
  // Wait a moment for the USB connection to establish

  while (!RYLR) {
    Serial.println("D:");
  }
  Serial.println("conneted");
  RYLR.print("AT\r\n");
  Serial.println("Sent 'AT\\r\\n' command. Waiting for response...");
  delay(500);
}
int lineindex = 0;
char message;
void loop() {
  if (RYLR.available() > 0) {
    String line = RYLR.readStringUntil(10, 1000);
    Serial.println(line);
    if (line[1] == 82 && line[2] == 67) {
      Serial.print("message:");
      message = line[10];
      Serial.println(message);
    }
    for (int i = 0; i < sizeof(line); ++i) {
      line[i] = 0;
    }
  }

  if (Serial.available()) {
    char c = Serial.read();
    RYLR.write(c);
  }
  if (message == 'D') {
    message = 'o';
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
}
