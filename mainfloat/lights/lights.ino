#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif
Adafruit_NeoPixel strip1(16, 10, NEO_RGB + NEO_KHZ800);
Adafruit_NeoPixel strip2(16, 11, NEO_RGB + NEO_KHZ800);
Adafruit_NeoPixel strip3(16, 9, NEO_RGB + NEO_KHZ800);
Adafruit_NeoPixel strip4(16, 8, NEO_RGB + NEO_KHZ800);
float NO = 0;
int R = 0;
int G = 0;
int B = 0;

void setup() {
    Serial1.begin(9600);
    strip1.begin();
    strip2.begin();
    strip3.begin();
    strip4.begin();
}

void loop() {
    // strip1.setPixelColor(random(0,16-1), strip1.Color(random(0,25)*10,
    // random(0,25)*10, random(0,25)*10));

    if (Serial1.available() > 0) {
        char c = Serial1.read();
        if (c == 'r') {
            R = 50;
            G = 0;
            B = 0;
        }
        if (c == 'g') {
            R = 0;
            G = 50;
            B = 0;
        }
        if (c == 'b') {
            R = 0;
            G = 0;
            B = 50;
        }
        if (c == 'w') {
            R = 50;
            G = 50;
            B = 50;
        }
        if (c == 'c') {
            R = 0;
            G = 50;
            B = 50;
        }
        if (c == 'y') {
            R = 50;
            G = 30;
            B = 0;
        }
        if (c == 'm') {
            R = 50;
            G = 0;
            B = 50;
        }
        if (c == 'k') {
            R = 0;
            G = 0;
            B = 0;
        }
    }
    strip1.clear();
    strip2.clear();
    strip3.clear();
    strip4.clear();
    for (int i = 0; i <= 4; i += 1) {
        strip1.setPixelColor(i*4+int(NO), strip1.Color(G, R, B));
        strip1.show(); // Send the updated pixel colors to the hardware.
        strip2.setPixelColor(i*4+int(NO), strip2.Color(G, R, B));
        strip2.show(); // Send the updated pixel colors to the hardware.
        strip3.setPixelColor(i*4+int(NO), strip3.Color(G, R, B));
        strip3.show();
        strip4.setPixelColor(i*4+int(NO), strip4.Color(G, R, B));
        strip4.show();
    }
    NO += 0.1;
    if (int(NO) == 4) {
        NO = 0;
    }
    delay(5);
}
