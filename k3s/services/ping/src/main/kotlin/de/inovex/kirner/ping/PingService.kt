package de.inovex.kirner.ping

import de.inovex.kirner.ping.config.ConfigProperties
import org.slf4j.LoggerFactory
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty
import org.springframework.http.HttpEntity
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Service
import org.springframework.web.client.RestTemplate


@Service
@ConditionalOnProperty("features.ping", havingValue = "true")
class PingService(private val config: ConfigProperties) {

    private val log = LoggerFactory.getLogger(PingService::class.java)

    @Scheduled(fixedRate = 5000)
    fun reportCurrentTime() {
        log.info("Sending Ping - timestamp: ${System.currentTimeMillis()}")

        RestTemplate().postForObject(
            "${config.host}/pong",
            HttpEntity<PingData>(PingData(System.currentTimeMillis())),
            Any::class.java
        )
        log.info("Received Pong - ${System.currentTimeMillis()}")
    }
}
