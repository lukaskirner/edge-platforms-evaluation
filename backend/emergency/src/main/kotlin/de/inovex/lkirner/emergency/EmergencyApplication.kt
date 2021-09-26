package de.inovex.lkirner.emergency

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.ConfigurationPropertiesScan
import org.springframework.boot.runApplication

@SpringBootApplication
@ConfigurationPropertiesScan
class EmergencyApplication

fun main(args: Array<String>) {
	runApplication<EmergencyApplication>(*args)
}
