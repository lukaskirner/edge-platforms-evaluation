import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
	id("org.springframework.boot") version "2.5.4"
	id("io.spring.dependency-management") version "1.0.11.RELEASE"
	id("com.google.cloud.tools.jib") version "3.1.4"

	kotlin("jvm") version "1.5.21"
	kotlin("plugin.spring") version "1.5.21"
}

group = "de.inovex.kirner"
version = "0.0.1-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_11

repositories {
	mavenCentral()
}

dependencies {
	// Spring Boot starter
	implementation("org.springframework.boot:spring-boot-starter-actuator")
	implementation("org.springframework.boot:spring-boot-starter-web")

	// Kotlin stuff
	implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
	implementation("org.jetbrains.kotlin:kotlin-reflect")
	implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")

	// ioFog
	implementation(files("libs/iofog-java-sdk-0.0.1.jar"))

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
		jvmTarget = "11"
	}
}

tasks.withType<Test> {
	useJUnitPlatform()
}
