package de.inovex.kirner.ping

import org.slf4j.LoggerFactory
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/pong")
@ConditionalOnProperty("features.pong", havingValue = "true")
class PongController {

    private val log = LoggerFactory.getLogger(PongController::class.java)

    @PostMapping
    fun pong(@RequestBody body: PingData): ResponseEntity<*> {
        val current = System.currentTimeMillis()
        val diff = current - body.timestamp
        log.info("Received Ping - timestamp: ${body.timestamp} -> $current | $diff")
        return ResponseEntity.noContent().build<Any>()
    }
}
