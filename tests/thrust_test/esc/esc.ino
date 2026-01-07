#include <Servo.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

#define SCREEN_WIDTH 128     // OLED display width, in pixels
#define SCREEN_HEIGHT 32     // OLED display height, in pixels
#define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3D  ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
#define DEBUG false

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Servo esc;

void setup() {
  // if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
  //   if (DEBUG) Serial.println(F("SSD1306 allocation failed"));
  //   for (;;)
  //     ;  // Don't proceed, loop forever
  // }
  // put your setup code here, to run once:
  esc.attach(9);
  esc.write(0);
  delay(1000);
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  for (int i = 90; i <= 160; i++) {
    delay(500);
    // display.clearDisplay();
    // display.setTextSize(1);
    // display.setTextColor(SSD1306_WHITE);
    // display.setCursor(0, 0);
    // //display.cp437(true);
    // display.println(i);
    Serial.println(i);
  
    esc.write(i);
  }
  digitalWrite(13,1);
;}

void loop() {
  esc.write(160);
  // put your main code here, to run repeatedly:
}