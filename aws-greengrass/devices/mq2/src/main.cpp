#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <AWSGreenGrassIoT.h>
#include <Adafruit_BMP280.h>
#define DIGITAL_PIN 32
#define ANALOG_PIN 33

const int publish_frequency = 5000; //Time in ms to publish sensor data

extern const char aws_root_ca[];
extern const char thingCA[];
extern const char thingKey[];


WiFiUDP ntpUDP;
IPAddress ip;

extern const char WIFI_SSID[];
extern const char WIFI_PASSWORD[];
extern const char AWSIOTURL[];
extern const char THING[];
char TOPIC_NAME[]= "sensor/mq2";  

AWSGreenGrassIoT * greengrass;
int status = WL_IDLE_STATUS;
char payload[512];
bool ConnectedToGGC = false;

Adafruit_BMP280 bmp;

const char JSONPAYLOAD[] = "{\"gasVal\": %f, \"isGas\": %i}"; 


void publishToGreengrass(String id, float gasVal, boolean isGas) {
    sprintf(payload,JSONPAYLOAD, gasVal, isGas);
    if(greengrass->publish(TOPIC_NAME, payload)) {        
        Serial.print("Publish Message: ");
        Serial.println(payload);
    } else {
        Serial.println("Publish failed");
    }  
}

void ConnToGGC(void) {
    ConnectedToGGC = false;

     while(ConnectedToGGC == false){
        greengrass = new AWSGreenGrassIoT(AWSIOTURL, THING, aws_root_ca, thingCA, thingKey);

        if(greengrass->connectToGG() == true) {
            Serial.println("Connected to AWS GreenGrass");
            ConnectedToGGC = true;
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

    // init MQ-2
    Serial.println("The sensor is warming up...");
    delay(30000);

    Serial.println("The sensor is warm up!");
    pinMode(DIGITAL_PIN, INPUT);
}


void loop() {
    if (greengrass->isConnected()){
        uint16_t gasVal = analogRead(ANALOG_PIN);  
        boolean isGas = !digitalRead(DIGITAL_PIN);
        gasVal = map(gasVal, 0, 1023, 0, 100);

        publishToGreengrass(THING, gasVal, isGas);
    } else {
        Serial.println("Greengrass not connected");
        ConnToGGC();
    }

    delay(publish_frequency);
}
