#define nano Serial3
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  // Initialize the second serial port for communication with another device
  nano.begin(115200);

  // Wait a moment for the USB connection to establish

  while (!nano) {
    Serial.println("D:");
  }
  delay(500);
}
void loop() {
  // put your main code here, to run repeatedly:
  
  if (Serial.available()) {
    char c = Serial.read();
    nano.write(c);
  }
}
