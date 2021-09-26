#include <Arduino.h>
#include <ArduinoJson.h>
#include <ThesisEdge.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>
#include "wifi_secrets.h"
#define LED_GREEN 32
#define LED_RED 33

// config for connecting to edge platform (WiFi, MQTT)
ThesisEdge edge_config = {
  .wifi_ssid = SECRET_SSID,
  .wifi_pass = SECRET_PASS,
  .mqtt_clientId_prefix = "sensor-bmp280-",
  .mqtt_broker = "master.fritz.box",
  .mqtt_port = 1883,
};

// schedule
const long interval = 1000;
unsigned long previousMillis = 0;

// bmp
Adafruit_BMP280 bmp;

// topic
const String publishTopic = "sensor/bmp280";

void setup() {
  // Initialize serial
  Serial.begin(9600);

  // activate pins
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_RED, HIGH);

  // connect to edge platform
  connectToEdge(&edge_config);

  // init BMP280
  if (!bmp.begin()) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }

  Serial.println("BMP280 connected!");
  Serial.println();

  // indicate ready status
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_GREEN, HIGH);
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    checkConnectionToEdge();

    DynamicJsonDocument doc(1024);
    doc["temperature"] = bmp.readTemperature();
    doc["pressure"] = bmp.readPressure() / 100;
    doc["altitude"] = bmp.readAltitude(1013.25);
    publishMessageToEdge(publishTopic, doc);
  }
}
