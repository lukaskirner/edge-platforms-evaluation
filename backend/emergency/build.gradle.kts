import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    val springBootVersion = "2.4.5"
    val kotlinVersion = "1.4.32"

	id("org.springframework.boot") version springBootVersion
    id("io.spring.dependency-management") version "1.0.11.RELEASE"
    id("com.google.cloud.tools.jib") version "3.0.0"

	kotlin("jvm") version kotlinVersion
	kotlin("plugin.spring") version kotlinVersion
}

group = "de.inovex.lkirner"
version = "0.0.1-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_11

repositories {
	mavenCentral()
}

dependencies {
    // spring starter
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-configuration-processor")
    implementation("org.springframework.boot:spring-boot-starter-data-redis")

    // redis
    implementation("redis.clients:jedis:3.6.0")

    // json
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")

    // kotlin
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")

    // mqtt
    implementation("org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.2.5")

    // test
	testImplementation("org.springframework.boot:spring-boot-starter-test")
}

jib {
    from {
        image = "docker.io/arm64v8/openjdk:11-slim" // <-- Important
    }
    to {
        tags = setOf("latest")
    }
    container {
        ports = listOf("8080")
    }
}

tasks.withType<KotlinCompile> {
	kotlinOptions {
		freeCompilerArgs = listOf("-Xjsr305=strict")
		jvmTarget = java.sourceCompatibility.toString()
	}
}

tasks.withType<Test> {
	useJUnitPlatform()
}
