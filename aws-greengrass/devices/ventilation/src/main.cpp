#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <AWSGreenGrassIoT.h>

#define FAN_PIN 14

const int period = 5000;

extern const char aws_root_ca[];
extern const char thingCA[];
extern const char thingKey[];

WiFiUDP ntpUDP;
IPAddress ip;

extern const char WIFI_SSID[];
extern const char WIFI_PASSWORD[];
extern const char AWSIOTURL[];
extern const char THING[];
char TOPIC_NAME[]= "actor/ventilation"; 

AWSGreenGrassIoT * greengrass;
int status = WL_IDLE_STATUS;
String receivedPayload = "";
bool ConnectedToGGC = false;
bool SubscribedToGGC = false;


static void subscribeCallback (int topicLen, char *topicName, int payloadLen, char *payLoad) {
    Serial.println("subscribeCallback");
    receivedPayload = payLoad;

    if (receivedPayload.indexOf("isOn") > 0) {
        if (receivedPayload.indexOf("true") > 0) {
            Serial.println("Switching ventilation on");
            digitalWrite(FAN_PIN, HIGH);
        } else if (receivedPayload.indexOf("false") > 0) {
            Serial.println("Switching ventilation off");
            digitalWrite(FAN_PIN, LOW);
        }
    }
}

void ConnToGGC(void) {
    ConnectedToGGC = false;

    while(ConnectedToGGC == false){
        greengrass = new AWSGreenGrassIoT(AWSIOTURL, THING, aws_root_ca, thingCA, thingKey);

        if(greengrass->connectToGG() == true) {
            Serial.println("Connected to AWS GreenGrass");
            ConnectedToGGC = true;
            delay(1000);

            while(SubscribedToGGC == false){
                if(greengrass->subscribe(TOPIC_NAME, subscribeCallback) == true) {
                    Serial.print("Subscribe to topic ");
                    Serial.print(TOPIC_NAME);
                    Serial.println(" was successful");
                    SubscribedToGGC = true;
                } else{
                    Serial.print("Subscribe to topic ");
                    Serial.print(TOPIC_NAME);
                    Serial.println(" failed");
                    SubscribedToGGC = false;
                }
                delay(1000); //wait for retry
            }
        } else {
            Serial.println("Connection to Greengrass failed, check if Greengrass core is on and connected to the WiFi");
        }

        delay(1000);
    }
}

void setup() {
    Serial.begin(115200);
    Serial.println("\n\nDevice started\n");
    
    while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to SSID: ");
        Serial.println(WIFI_SSID);
        status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
        delay(3000);
    }

    Serial.println("Connected to local wifi");

    ip = WiFi.localIP();
    Serial.print("local ip address of this ESP32 = ");
    Serial.println(ip);

    delay(1000);
    ConnToGGC();

    // configure GPIO
    pinMode(FAN_PIN, OUTPUT);
}

void loop() {
    if (!greengrass->isConnected()){
        Serial.println("Greengrass not connected");
        ConnToGGC();
    }

    delay(period);      
}
