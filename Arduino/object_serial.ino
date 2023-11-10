#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <LedControl.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); 
LedControl lc = LedControl(12, 11, 10, 1); 
void setup() {
  lcd.init();                      
  lcd.backlight();              
  Serial.begin(9600);      
  lc.shutdown(0, false);  
  lc.setIntensity(0, 6);
  lc.clearDisplay(0);
}

void loop() {
  if (Serial.available() > 0) {
    String receivedData = Serial.readStringUntil('\n'); 
    if (receivedData == "Warning!") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Warning!");
      displayOnMatrix();
    }else if(receivedData == "Normal"){
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Normal");
      clearMatrix(); 
    }

  }
}


void displayOnMatrix() {
  for (int i = 0; i < 8; i++) {
    for (int j = 0; j < 8; j++) {
      lc.setLed(0, i, j, true);
    }
  }
}

void clearMatrix() {
  for (int i = 0; i < 8; i++) {
    for (int j = 0; j < 8; j++) {
      lc.setLed(0, i, j, false);
    }
  }
}