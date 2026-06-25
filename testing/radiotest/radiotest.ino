#include <AltSoftSerial.h>

AltSoftSerial RYLR;
void sendradiomessage(String msg) {
    RYLR.print("AT+SEND=");
    RYLR.print("82");
    RYLR.print(",");
    RYLR.print(msg.length());
    RYLR.print(",");
    RYLR.print(msg);
    RYLR.print("\r\n");
}
void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    Serial.println("inti????");

    // Initialize the second serial port for communication with another device
    RYLR.begin(9600);

    // Wait a moment for the USB connection to establish
    delay(2000);
    

    RYLR.print("AT\r\n");
    Serial.println("Sent 'AT\\r\\n' command. Waiting for response...");
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
            if (line[1] == 82 && line[2] == 67) {
                Serial.print("message:");
                Serial.println(line[10]);
            }
        }
    }

    if (Serial.available()) {
        char c = Serial.read();
        Serial.println(c);
        RYLR.write(c);
    }
}
