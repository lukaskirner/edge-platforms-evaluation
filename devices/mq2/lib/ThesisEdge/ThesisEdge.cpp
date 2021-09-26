#include "ThesisEdge.h"
#include <PubSubClient.h>
#include <WiFi.h>
#include <SPI.h>

// connection config
ThesisEdge* config;

// wifi
WiFiClient wifiClient;

// mqtt
PubSubClient mqttClient(wifiClient);

// unique ids
String mac;
String clientId;

void connectToWiFi(String, String);
void connectToMQTT(String, int, const String);

void checkConnectionToEdge() {
  if (config == nullptr) {
    Serial.println("No config present. Call `connect(ThesisEdge*)` before.");
    return;
  }

  if (!WiFi.isConnected()) {
    connectToWiFi(config->wifi_ssid, config->wifi_pass);
  }

  if (!mqttClient.connected()) {
    connectToMQTT(config->mqtt_broker, config->mqtt_port, clientId.c_str());
  }
}

void connectToEdge(ThesisEdge* data) {
  config = data;
  connectToWiFi(config->wifi_ssid, config->wifi_pass);

  clientId = config->mqtt_clientId_prefix + mac;
  connectToMQTT(config->mqtt_broker, config->mqtt_port, clientId.c_str());
}

void connectToWiFi(String ssid, String pass) {
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  while (WiFi.begin(ssid.c_str(), pass.c_str()) != WL_CONNECTED) {
    Serial.print(".");
    delay(5000);
  }

  mac = WiFi.macAddress();
  Serial.println("You're connected to the network");
  Serial.println();
}

void connectToMQTT(String broker, int port, const String clientId) {
  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  mqttClient.setServer(broker.c_str(), port);
  if (!mqttClient.connect(clientId.c_str())) {
    Serial.print("MQTT connection failed! Error code = ");
    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}

void publishMessageToEdge(const String topic, DynamicJsonDocument doc) {
  if (mqttClient.connected()) {
    doc["deviceId"] = mac; 
    String message;
    serializeJson(doc, message);

    if (!mqttClient.publish(topic.c_str(), message.c_str())) {
      Serial.println("Could not send message!");
    }
  } else {
    Serial.println("Not connected to MQTT broker");
  }
}