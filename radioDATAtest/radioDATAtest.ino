#define RYLR Serial2
#include <SD.h>
#include <SPI.h>
const int chipSelect = BUILTIN_SDCARD;

void setup() {

  // put your setup code here, to run once:

  Serial.begin(115200);
  // Initialize the second serial port for communication with another device
  RYLR.begin(115200);

  // Wait a moment for the USB connection to establish

  while (!RYLR) {
    Serial.println("D:");
  }
  Serial.println("conneted");
  RYLR.print("AT\r\n");
  Serial.println("Sent 'AT\\r\\n' command. Waiting for response...");
  delay(500);
}
char line[64];
int lineindex = 0;
char message;
void loop() {
  // put your main code here, to run repeatedly:
  if (RYLR.available() > 0) {
    char c = RYLR.read();
    //Serial.print(c);
    line[lineindex] = c;
    lineindex++;
    if (c == 10) {
      lineindex = 0;
      // Serial.print("line:");
      // Serial.println(line);
      if (line[1] == 82 && line[2] == 67) {
        Serial.print("message:");
        message = line[10];
        Serial.println(message);
      }
    }
  }

  if (Serial.available()) {
    char c = Serial.read();
    RYLR.write(c);
  }
  if (message == 'D') {
    Serial.println("yippee");
    File myFile = SD.open("data.txt");
    if (myFile) {
      Serial.println("Reading data.txt:");
      while (myFile.available()) {
        char c = myFile.read();
        line[lineindex] = c;
        lineindex++;
        if (c == 10) {
          line = "";
        }
      }
      RYLR.print("AT+SEND=82,");
      RYLR.print();
      message = 'o';
    }
  }
