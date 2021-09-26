package de.inovex.lkirner.emergency.ventilation

import org.springframework.data.redis.core.RedisHash

@RedisHash("ventilation")
data class VentilationLock(
    val id: String,
    val state: VentilationState,
)
