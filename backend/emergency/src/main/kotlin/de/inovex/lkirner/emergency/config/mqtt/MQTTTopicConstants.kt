package de.inovex.lkirner.emergency.config.mqtt

enum class MQTTTopicConstants(val topic: String) {
    SENSOR_BMP280("sensor/bmp280/#"),
    SENSOR_MQ2("sensor/mq2/#"),
    VENTILATION("actor/ventilation")
}
