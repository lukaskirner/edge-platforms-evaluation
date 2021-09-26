package de.inovex.lkirner.emergency.config.mqtt

import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.boot.context.properties.ConstructorBinding

@ConstructorBinding
@ConfigurationProperties(prefix = "mqtt")
data class MQTTProperties(
    val hostName: String?,
    val port: Int?,
    val username: String?,
    val password: String?
)
