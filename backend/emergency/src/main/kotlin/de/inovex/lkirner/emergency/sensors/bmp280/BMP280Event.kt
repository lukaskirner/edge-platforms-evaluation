package de.inovex.lkirner.emergency.sensors.bmp280

import com.fasterxml.jackson.annotation.JsonIgnoreProperties

@JsonIgnoreProperties(ignoreUnknown = true)
data class BMP280Event (
    val temperature: Float,
    val pressure: Float,
    val altitude: Float
)
