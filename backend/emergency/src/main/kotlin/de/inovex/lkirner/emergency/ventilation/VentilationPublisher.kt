package de.inovex.lkirner.emergency.ventilation

import de.inovex.lkirner.emergency.config.mqtt.MQTTTopicConstants
import de.inovex.lkirner.emergency.sensors.bmp280.BMP280EventHandler
import org.eclipse.paho.client.mqttv3.MqttClient
import org.eclipse.paho.client.mqttv3.MqttMessage
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service

@Service
class VentilationPublisher(
    private val client: MqttClient,
    private val repository: VentilationLockRepository
) {

    private val log = LoggerFactory.getLogger(VentilationPublisher::class.java)

    private var ventilationIsOn: Boolean = false

    fun startVentilationWithDeviceId(deviceId: String) {
        changeVentilationState(deviceId, VentilationState.ON)
    }

    fun stopVentilationWithDeviceId(deviceId: String) {
        changeVentilationState(deviceId, VentilationState.OFF)
    }

    private fun changeVentilationState(deviceId: String, newState: VentilationState) {
        getLockByDeviceId(deviceId).ifPresentOrElse({
            if (newState == VentilationState.OFF) repository.delete(it)
        }, {
            if (newState == VentilationState.ON) repository.save(VentilationLock(id = deviceId, newState))
        })

        if (hasLocks()) {
            if (!ventilationIsOn) {
                publishON()
                log.info("Ventilation: ON")
                ventilationIsOn = true
            }
        } else {
            if (ventilationIsOn) {
                publishOFF()
                log.info("Ventilation: OFF")
                ventilationIsOn = false
            }
        }
    }

    private fun hasLocks() = repository.findAll().count() > 0

    private fun getLockByDeviceId(deviceId: String) = repository.findById(deviceId)

    private fun publishON() = client.publish(MQTTTopicConstants.VENTILATION.topic, MqttMessage(VentilationState.ON.value.toByteArray()))

    private fun publishOFF() = client.publish(MQTTTopicConstants.VENTILATION.topic, MqttMessage(VentilationState.OFF.value.toByteArray()))
}
