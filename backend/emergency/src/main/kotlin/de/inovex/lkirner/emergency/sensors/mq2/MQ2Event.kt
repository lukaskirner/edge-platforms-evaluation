package de.inovex.lkirner.emergency.sensors.mq2

import com.fasterxml.jackson.annotation.JsonIgnoreProperties

@JsonIgnoreProperties(ignoreUnknown = true)
data class MQ2Event (
    val isGas: Boolean,
    val gasVal: Float
)
