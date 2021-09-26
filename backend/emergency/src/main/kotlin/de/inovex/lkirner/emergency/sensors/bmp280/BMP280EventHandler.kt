package de.inovex.lkirner.emergency.sensors.bmp280

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
class BMP280EventHandler(
    mqttClient: MqttClient,
    private val ventilationPublisher: VentilationPublisher
): MQTTMessageHandler(mqttClient, MQTTTopicConstants.SENSOR_BMP280.topic) {

    private val log = LoggerFactory.getLogger(BMP280EventHandler::class.java)

    private val TEMP_TRESHOLD: Float = 30F

    override fun subscribe(topic: String, message: MqttMessage) {
        log.info("Received message [topic: $topic, Qos: ${message.qos}, payload: ${String(message.payload)}]")

        val mapper = jacksonObjectMapper()
        val deviceId = topic.replace("/", "-") // format: sensor-bmp280-<mac>
        val event: BMP280Event = mapper.readValue(message.payload)

        if (event.temperature > TEMP_TRESHOLD) {
            ventilationPublisher.startVentilationWithDeviceId(deviceId)
        } else {
            ventilationPublisher.stopVentilationWithDeviceId(deviceId)
        }
    }
}
