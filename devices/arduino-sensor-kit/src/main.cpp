#include <Arduino.h>
#include "Adafruit_Sensor.h"
#include "Arduino_SensorKit.h"

void setup() {
  Serial.begin(9600);
  Environment.begin();
}

void loop() {
  Serial.print("Temperature = ");
  Serial.print(Environment.readTemperature());
  Serial.println(" C");
  Serial.print("Humidity = ");
  Serial.print(Environment.readHumidity());
  Serial.println(" %");
  delay(2000);
}
