/*
  Use the Qwiic Scale to read load cells and scales
  By: Nathan Seidle @ SparkFun Electronics
  Date: March 3rd, 2019
  License: This code is public domain but you buy me a beer if you use this
  and we meet someday (Beerware license).

  This example shows how to setup a scale complete with zero offset (tare),
  and linear calibration.
*/

#include <Wire.h>
#include <EEPROM.h>  //Needed to record user settings

#include "SparkFun_Qwiic_Scale_NAU7802_Arduino_Library.h"  // Click here to get the library: http://librarymanager/All#SparkFun_NAU8702
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128  // OLED display width, in pixels
#define SCREEN_HEIGHT 32  // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C  ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
NAU7802 myScale;  //Create instance of the NAU7802 class

// NOTE: The NEWTON_FACTOR was unused in the original code's weight calculation,
// but it was used to multiply the raw reading which makes no sense for weight.
// I have removed its use in loop() but kept the definition just in case it was
// meant for something else later.
const float NEWTON_FACTOR = 9.80665;

//EEPROM locations to store 4-byte variables
#define EEPROM_SIZE 100                //Allocate 100 bytes of EEPROM
#define LOCATION_CALIBRATION_FACTOR 0  //Float, requires 4 bytes of EEPROM
#define LOCATION_ZERO_OFFSET 10        //Must be more than 4 away from previous spot. int32_t, requires 4 bytes of EEPROM

bool settingsDetected = false;  //Used to prompt user to calibrate their scale
bool print = false;
//Create an array to take average of weights. This helps smooth out jitter.
#define AVG_SIZE 4
float avgWeights[AVG_SIZE];
byte avgWeightSpot = 0;
float starttime = 0;

// Function prototypes (needed because the functions are defined later)
void calibrateScale(void);
void recordSystemSettings(void);
void readSystemSettings(void);

void setup() {
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;  // Don't proceed, loop forever
  }
  Serial.begin(115200);
  Serial.println("Qwiic Scale Example");

  Wire.begin();
  Wire.setClock(400000);  //Qwiic Scale is capable of running at 400kHz if desired

  if (myScale.begin() == false) {
    Serial.println("Scale not detected. Please check wiring. Freezing...");
    while (1)
      ;
  }
  Serial.println("Scale detected!");

  readSystemSettings();  //Load zeroOffset and calibrationFactor from EEPROM

  myScale.setSampleRate(NAU7802_SPS_320);  //Increase to max sample rate
  myScale.calibrateAFE();                  //Re-cal analog front end when we change gain, sample rate, or channel

  Serial.print("Zero offset: ");
  Serial.println(myScale.getZeroOffset());
  Serial.print("Calibration factor: ");
  Serial.println(myScale.getCalibrationFactor());

  Serial.println("\r\nPress 't' to Tare or Zero the scale.");
}

void loop() {
  if (myScale.available() == true) {
    // The line below was multiplying the raw reading by NEWTON_FACTOR, which is likely wrong.
    // int32_t currentReading = myScale.getReading() * NEWTON_FACTOR; // Faulty line

    // The raw reading is only useful if you want to see the uncalibrated value.
    // The currentWeight already applies the calibration factor.
    // If you need the raw reading: int32_t currentReading = myScale.getReading();

    // myScale.getWeight() returns the weight in the unit you set (e.g., grams, kg, oz, lb).
    // The -1 factor is likely to correct for the load cell wiring direction.
    float currentWeight = myScale.getWeight(true, 8, 1000) * -1;

    avgWeights[avgWeightSpot++] = currentWeight;
    if (avgWeightSpot == AVG_SIZE) avgWeightSpot = 0;

    float avgWeight = 0;
    for (int x = 0; x < AVG_SIZE; x++)
      avgWeight += avgWeights[x];
    avgWeight /= AVG_SIZE;

    display.clearDisplay();

    display.setTextSize(1);               // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE);  // Draw white text
    display.setCursor(0, 0);              // Start at top-left corner
    display.print(F("Weight:"));
    display.println(avgWeight, 2);
    display.display();

    if (Serial.available()) {
      byte incoming = Serial.read();
      if (incoming == 'p') {
        print = true;
      }
      if (incoming == 's') {
        starttime = millis();
        print = false;
        Serial.println("stop");
      }

      // Handle 't' and 'c' inputs here too, even if print is false
      if (incoming == 't')  //Tare the scale
        myScale.calculateZeroOffset();
      else if (incoming == 'c')  //Calibrate
      {
        calibrateScale();
      }
    }

    if (print) {
      Serial.print("[");
      Serial.print(avgWeight, 2);  //Print 2 decimal places
      Serial.print("]");
      Serial.print("(");
      // Corrected starttime spelling in the print statement
      Serial.print((float)(millis() - starttime) / 1000, 1);  //Print 1 decimal place (seconds since 's' was pressed)
      Serial.print(")");
      Serial.println();
    }

    if (settingsDetected == false) {
      Serial.print("\tScale not calibrated. Press 'c'.");
    }

    


    // Removed redundant Serial.available() check and t/c handling
  }
}

// Gives user the ability to set a known weight on the scale and calculate a calibration factor
// THIS FUNCTION MUST BE OUTSIDE loop()
void calibrateScale(void) {
  Serial.println();
  Serial.println();
  Serial.println(F("Scale calibration"));

  Serial.println(F("Setup scale with no weight on it. Press a key when ready."));
  while (Serial.available()) Serial.read();   //Clear anything in RX buffer
  while (Serial.available() == 0) delay(10);  //Wait for user to press key

  myScale.calculateZeroOffset(64);  //Zero or Tare the scale. Average over 64 readings.
  Serial.print(F("New zero offset: "));
  Serial.println(myScale.getZeroOffset());

  Serial.println(F("Place known weight on scale. Press a key when weight is in place and stable."));
  while (Serial.available()) Serial.read();   //Clear anything in RX buffer
  while (Serial.available() == 0) delay(10);  //Wait for user to press key

  Serial.print(F("Please enter the weight, without units, currently sitting on the scale (for example '4.25'): "));
  while (Serial.available()) Serial.read();   //Clear anything in RX buffer
  while (Serial.available() == 0) delay(10);  //Wait for user to press key

  //Read user input
  float weightOnScale = Serial.parseFloat();
  Serial.println(weightOnScale, 2);  // Echo the value back to the user

  myScale.calculateCalibrationFactor(weightOnScale, 64);  //Tell the library how much weight is currently on it
  Serial.print(F("New cal factor: "));
  Serial.println(myScale.getCalibrationFactor(), 2);

  Serial.print(F("New Scale Reading: "));
  Serial.println(myScale.getWeight(true, 8, 1000), 2);

  recordSystemSettings();  //Commit these values to EEPROM

  settingsDetected = true;
}

// Record the current system settings to EEPROM
// THIS FUNCTION MUST BE OUTSIDE loop()
void recordSystemSettings(void) {
  //Get various values from the library and commit them to NVM
  EEPROM.put(LOCATION_CALIBRATION_FACTOR, myScale.getCalibrationFactor());
  EEPROM.put(LOCATION_ZERO_OFFSET, myScale.getZeroOffset());
}

// Reads the current system settings from EEPROM
// If anything looks weird, reset setting to default value
// THIS FUNCTION MUST BE OUTSIDE loop()
void readSystemSettings(void) {
  float settingCalibrationFactor;  //Value used to convert the load cell reading to lbs or kg
  int32_t settingZeroOffset;       //Zero value that is found when scale is tared

  //Look up the calibration factor
  EEPROM.get(LOCATION_CALIBRATION_FACTOR, settingCalibrationFactor);
  if (settingCalibrationFactor == 0xFFFFFFFF) {
    settingCalibrationFactor = 1.0;  //Default to 1.0
    EEPROM.put(LOCATION_CALIBRATION_FACTOR, settingCalibrationFactor);
  }

  //Look up the zero tare point
  EEPROM.get(LOCATION_ZERO_OFFSET, settingZeroOffset);
  if (settingZeroOffset == 0xFFFFFFFF) {
    settingZeroOffset = 0;  //Default to 0 - i.e. no offset
    EEPROM.put(LOCATION_ZERO_OFFSET, settingZeroOffset);
  }

  //Pass these values to the library
  myScale.setCalibrationFactor(settingCalibrationFactor);
  myScale.setZeroOffset(settingZeroOffset);

  settingsDetected = true;  //Assume for the moment that there are good cal values
  if (settingCalibrationFactor == 1.0 || settingZeroOffset == 0)
    settingsDetected = false;  //Defaults detected. Prompt user to cal scale.
}