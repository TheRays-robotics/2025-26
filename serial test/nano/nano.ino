#define bigT Serial
void setup() {
  // put your setup code here, to run once:
  // Initialize the second serial port for communication with another device
  bigT.begin(9600);

  // Wait a moment for the USB connection to establish

  while (!bigT) {
    Serial.println("D:");
  }
  delay(500);
}
void loop() {
  // put your main code here, to run repeatedly:
  
  if (bigT.available() > 0) {
    //char c = bigT.read();
    int I = Serial.parseInt();
    digitalWrite(I,HIGH);
    Serial.println(I);
    
  }

}
