package de.inovex.lkirner.emergency.config.redis

import org.springframework.boot.autoconfigure.data.redis.RedisProperties
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.context.annotation.Primary
import org.springframework.data.redis.connection.jedis.JedisConnectionFactory
import org.springframework.data.redis.core.RedisTemplate


@Configuration
class RedisConfig {

    @Bean
    @Primary
    fun redisProperties() = RedisProperties()

    @Bean
    fun jedisConnectionFactory() = JedisConnectionFactory().apply {
        hostName = redisProperties().host
        port = redisProperties().port
        setPassword(redisProperties().password)
    }

    @Bean
    fun redisTemplate(): RedisTemplate<String, Any> {
        val template = RedisTemplate<String, Any>()
        template.setConnectionFactory(jedisConnectionFactory())
        return template
    }
}
