package de.inovex.kirner.ping

import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.stereotype.Component

@Component
@ConfigurationProperties(prefix = "features")
data class FeatureConfigProperties(
    var ping: Boolean = false,
    var pong: Boolean = false
)


