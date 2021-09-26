package de.inovex.lkirner.emergency.sensors.mq2

import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import de.inovex.lkirner.emergency.config.mqtt.MQTTMessageHandler
import de.inovex.lkirner.emergency.config.mqtt.MQTTTopicConstants
import de.inovex.lkirner.emergency.ventilation.VentilationPublisher
import org.eclipse.paho.client.mqttv3.MqttClient
import org.eclipse.paho.client.mqttv3.MqttMessage
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service

@Service
class MQ2EventHandler(
    mqttClient: MqttClient,
    private val ventilationPublisher: VentilationPublisher
): MQTTMessageHandler(mqttClient, MQTTTopicConstants.SENSOR_MQ2.topic) {

    private val log = LoggerFactory.getLogger(MQ2EventHandler::class.java)

    override fun subscribe(topic: String, message: MqttMessage) {
        log.info("Received message [topic: $topic, Qos: ${message.qos}, payload: ${String(message.payload)}]");

        val mapper = jacksonObjectMapper()
        val deviceId = topic.replace("/", "-") // format: sensor-mq2-<mac>
        val event: MQ2Event = mapper.readValue(message.payload)

        if (event.isGas) {
            ventilationPublisher.startVentilationWithDeviceId(deviceId)
        } else {
            ventilationPublisher.stopVentilationWithDeviceId(deviceId)
        }
    }
}
