package de.inovex.kirner.ping.config

import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.stereotype.Component

@Component
@ConfigurationProperties(prefix = "pong")
data class ConfigProperties(
    var host: String = "127.0.0.1:8080",
)
