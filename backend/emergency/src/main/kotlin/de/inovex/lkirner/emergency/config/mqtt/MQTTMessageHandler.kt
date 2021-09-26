package de.inovex.lkirner.emergency.config.mqtt

import org.eclipse.paho.client.mqttv3.MqttClient
import org.eclipse.paho.client.mqttv3.MqttMessage

abstract class MQTTMessageHandler(mqttClient: MqttClient, topic: String) {

    init {
        mqttClient.subscribe(topic, this::subscribe)
    }

    @Throws(Exception::class)
    abstract fun subscribe(topic: String, message: MqttMessage)
}
