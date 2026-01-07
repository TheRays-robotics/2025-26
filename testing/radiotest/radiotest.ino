#define RYLR Serial2
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
void loop() {
  // put your main code here, to run repeatedly:
  if (RYLR.available() > 0) {
    char c = RYLR.read();
    Serial.print(c);
    line[lineindex] = c;
    lineindex++;
    if (c == 10) {
      lineindex = 0;
      Serial.print("line:");
      Serial.println(line);
      if (line[1]==82 && line[2]==67) {
        Serial.print("message:");
        Serial.println(line[10]);
      }
    }
  }

  if (Serial.available()) {
    char c = Serial.read();
    RYLR.write(c);
  }
}
