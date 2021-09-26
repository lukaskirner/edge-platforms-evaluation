package de.inovex.kirner.ping

import org.eclipse.iofog.api.listener.IOFogAPIListener
import org.eclipse.iofog.elements.IOMessage
import org.slf4j.LoggerFactory
import javax.json.JsonObject

class MessageListener: IOFogAPIListener {

    private val log = LoggerFactory.getLogger(IOFogAPIListener::class.java)

    override fun onMessages(messages: MutableList<IOMessage>) {
        log.info("onMessages: ${messages.size}")
        messages.forEach { println(it.toJson()) }
    }

    override fun onMessageReceipt(id: String, timestamp: Long) {
        log.info("onMessageReceipt - timestamp: $timestamp")
    }

    override fun onMessagesQuery(p0: Long, p1: Long, p2: MutableList<IOMessage>) {
        log.info("onMessagesQuery")
    }

    override fun onError(p0: Throwable) {
        log.info("onError")
    }

    override fun onBadRequest(p0: String) {
        log.info("onBadRequest")
    }

    override fun onNewConfig(p0: JsonObject) {
        log.info("onNewConfig")
    }

    override fun onNewConfigSignal() {
        log.info("onNewConfigSignal")
    }
}