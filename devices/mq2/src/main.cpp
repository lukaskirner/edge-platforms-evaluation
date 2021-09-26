#include <Arduino.h>
#include <ArduinoJson.h>
#include <ThesisEdge.h>
#include <Wire.h>
#include <SPI.h>
#include "wifi_secrets.h"

// config for connecting to edge platform (WiFi, MQTT)
ThesisEdge edge_config = {
  .wifi_ssid = SECRET_SSID,
  .wifi_pass = SECRET_PASS,
  .mqtt_clientId_prefix = "sensor-mq2-",
  .mqtt_broker = "master.fritz.box",
  .mqtt_port = 1883,
};

// schedule
const long interval = 1000;
unsigned long previousMillis = 0;

// topic
const String publishTopic = "sensor/mq2";

// sensor stuff
#define DIGITAL_PIN 32
#define ANALOG_PIN 33

void setup() {
  // Initialize serial
  Serial.begin(9600);

  // connect to edge platform
  connectToEdge(&edge_config);

  // init MQ-2
  Serial.println("The sensor is warming up...");
  delay(30000);

  Serial.println("The sensor is warm up!");
  pinMode(DIGITAL_PIN, INPUT);
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    checkConnectionToEdge();

    uint16_t gasVal = analogRead(ANALOG_PIN);  
    boolean isGas = !digitalRead(DIGITAL_PIN);
    gasVal = map(gasVal, 0, 1023, 0, 100);
    
    DynamicJsonDocument doc(1024);
    doc["isGas"] = isGas;
    doc["gasVal"] = gasVal;
    publishMessageToEdge(publishTopic, doc);
  }
}