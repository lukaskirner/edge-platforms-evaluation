package de.inovex.kirner.ping

import de.inovex.kirner.ping.config.ConfigProperties
import org.eclipse.iofog.api.IOFogClient
import org.eclipse.iofog.elements.IOMessage
import org.slf4j.LoggerFactory
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Service

@Service
@ConditionalOnProperty("features.ping", havingValue = "true")
class PingService(config: ConfigProperties) {

    private val log = LoggerFactory.getLogger(PingService::class.java)
    private val client: IOFogClient = IOFogClient(config.host, config.port, config.containerid)

    init {
        client.openMessageWebSocket(MessageListener())
    }

    @Scheduled(fixedRate = 5000)
    fun reportCurrentTime() {
        val msg = generateNewIOMessage()
        log.info("Sending IOMessage - timestamp: ${System.currentTimeMillis()}")
        client.sendMessageToWebSocket(msg)
    }

    private fun generateNewIOMessage(): IOMessage {
        val message = IOMessage()
        message.id = ""
        message.tag = ""
        message.groupId = ""
        message.sequenceNumber = 0
        message.sequenceTotal = 0
        message.priority = 0
        message.timestamp = System.currentTimeMillis()
        message.publisher = "ping"
        message.authId = ""
        message.authGroup = ""
        message.chainPosition = 0
        message.hash = ""
        message.previousHash = ""
        message.nonce = ""
        message.difficultyTarget = 0
        message.infoType = ""
        message.infoFormat = ""
        message.contextData = byteArrayOf()
        message.contentData = byteArrayOf()
        return message
    }
}