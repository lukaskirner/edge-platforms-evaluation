#ifndef __THESIS_EDGE_H__
#define __THESIS_EDGE_H__

#include <Arduino.h>
#include <ArduinoJson.h>

struct ThesisEdge {
  String wifi_ssid;
  String wifi_pass;
  String mqtt_clientId_prefix;
  String mqtt_broker;
  int mqtt_port;
};

void checkConnectionToEdge();
void connectToEdge(ThesisEdge*);
void publishMessageToEdge(const String, DynamicJsonDocument);

#endif