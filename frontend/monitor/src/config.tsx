import mqtt from 'mqtt'

export function getMQTTHost(): string {
  return "ws://mqtt.edge.home"
  // if (process.env.NODE_ENV === 'production') { return "ws://mqtt.edge.home" }
  // return "wss://test.mosquitto.org"
}

export function getMQTTConfig(): mqtt.IClientOptions {
  return {port: 8083, protocol: "ws", path: "/mqtt", keepalive: 30}
  // if (process.env.NODE_ENV === 'production') { return {port: 8083, protocol: "ws", path: "/mqtt", keepalive: 30} }
  // return {port: 8081, protocol: "wss", keepalive: 30}
}

export function getAPIHost(): string {
  if (process.env.NODE_ENV === 'production') { return "http://monitor.edge.home" }
  return ""
}
