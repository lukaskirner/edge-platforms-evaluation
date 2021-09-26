#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "wifi_secrets.h"

#define FAN_PIN 14

// wifi
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS; 
WiFiClient wifiClient;

// mqtt
const char broker[] = "node2.fritz.box";
int port = 1883;
const char topic[] = "actor/ventilation";
PubSubClient mqttClient(wifiClient);

// unique ids
String mac;
String clientId;

void callback(char* topic, byte* payload, unsigned int length);

void setup() {
  // Initialize serial
  Serial.begin(9600);

  // attempt to connect to Wifi network:
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }

  Serial.println("You're connected to the network");
  Serial.println();

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  mqttClient.setServer(broker, port);
  mqttClient.setCallback(callback);

  clientId = "actor-ventilation-" + mac;
  if (!mqttClient.connect(clientId.c_str())) {
    Serial.print("MQTT connection failed! Error code = ");
    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();


  Serial.print("Subscribing to topic: ");
  Serial.println(topic);
  Serial.println();

  if (!mqttClient.subscribe(topic)) {
    Serial.print("MQTT subscription failed - topic: ");
    Serial.println(topic);
    Serial.println();
    while (1);
  }

  Serial.println("Waiting for messages on topic ...");

  // configure GPIO
  pinMode(FAN_PIN, OUTPUT);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");

  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  if(!strncmp((char *)payload, "true", length)){
    Serial.println("Switching ventilation on");
    digitalWrite(FAN_PIN, HIGH);
  }
  else if(!strncmp((char *)payload, "false", length)){
    Serial.println("Switching ventilation off");
    digitalWrite(FAN_PIN, LOW);
  }
}

void loop() {
  mqttClient.loop();        
}
