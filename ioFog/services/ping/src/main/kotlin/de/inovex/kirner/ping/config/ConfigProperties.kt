package de.inovex.kirner.ping.config

import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.stereotype.Component

@Component
@ConfigurationProperties(prefix = "iofog")
data class ConfigProperties(
    var host: String = "127.0.0.1",
    var port: Int = 54321,
    var containerid: String = "TEST_CONTAINER_ID"
)
