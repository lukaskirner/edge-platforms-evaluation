package de.inovex.lkirner.emergency.config.mqtt

import org.eclipse.paho.client.mqttv3.MqttClient
import org.eclipse.paho.client.mqttv3.MqttConnectOptions
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration


@Configuration
class MQTTConfiguration {

    private final val CLIENT_ID = "emergency-client"

    @Bean
    fun mqttClient(properties: MQTTProperties) = MqttClient(String.format("tcp://%s:%s", properties.hostName, properties.port), CLIENT_ID, MemoryPersistence()).apply {
        val options = MqttConnectOptions()
        options.isAutomaticReconnect = true
        options.isCleanSession = true
        options.connectionTimeout = 10

        if (!properties.username.isNullOrEmpty()) {
            options.userName = properties.username
        }

        if (!properties.password.isNullOrEmpty()) {
            options.password = properties.password.toCharArray()
        }
        connect(options)
    }
}
