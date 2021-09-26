#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <AWSGreenGrassIoT.h>
#include <Adafruit_BMP280.h>
#define LED_GREEN 32
#define LED_RED 33

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
char TOPIC_NAME[]= "sensor/bmp280";  

AWSGreenGrassIoT * greengrass;
int status = WL_IDLE_STATUS;
char payload[512];
bool ConnectedToGGC = false;

Adafruit_BMP280 bmp;

const char JSONPAYLOAD[] = "{\"temperature\": %f, \"pressure\": %f, \"altitude\": %f}"; 


void publishToGreengrass(String id, float temperature, float pressure, float altitude) {
    sprintf(payload,JSONPAYLOAD, temperature, pressure, altitude);
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
    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_GREEN, LOW);

    
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

    // init BMP280
    if (!bmp.begin()) {
        Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
        while (1);
    }

    Serial.println("BMP280 connected!");

    // indicate ready status
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_GREEN, HIGH);
}


void loop() {
    if (greengrass->isConnected()){
        float temperature = bmp.readTemperature();
        float pressure = bmp.readPressure() / 100;
        float altitude = bmp.readAltitude(1013.25);

        publishToGreengrass(THING, temperature, pressure, altitude);
    } else {
        Serial.println("Greengrass not connected");
        ConnToGGC();
    }

    delay(publish_frequency);
}
