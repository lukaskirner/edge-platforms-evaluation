package de.inovex.kirner.ping

import de.inovex.kirner.ping.config.ConfigProperties
import org.eclipse.iofog.api.IOFogClient
import org.slf4j.LoggerFactory
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Service

@Service
@ConditionalOnProperty("features.pong", havingValue = "true")
class PongService(config: ConfigProperties) {

    private val log = LoggerFactory.getLogger(PongService::class.java)
    private val client: IOFogClient = IOFogClient(config.host, config.port, config.containerid)

    init {
        log.info("Open Message WebSocket")
        client.openMessageWebSocket(MessageListener())
    }

    @Scheduled(fixedRate = 5000)
    fun reportCurrentTime() {
        client.fetchNextMessage(MessageListener())
    }
}