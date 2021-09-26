import React, { useEffect, useState } from 'react';
import './App.scss';
import Monitor, { MonitorHandle } from './monitor/Monitor'
import mqtt, { MqttClient } from 'mqtt'
import { useRef } from 'react';
import { getMQTTConfig, getMQTTHost } from '../config';

export default function App() {
  const [client, setClient] = useState<MqttClient | null>(null);
  const [connectStatus, setConnectStatus] = useState<string | null>(null);
  const monitorRef = useRef<MonitorHandle>(null)

  const mqttConnect = (host: string, mqttOption: mqtt.IClientOptions) => {
    setConnectStatus('Connecting');
    setClient(mqtt.connect(host, mqttOption));
  };

  const mqttSub = (subscription: mqtt.ISubscription) => {
    if (client) {
      const { topic, qos } = subscription;
      client.subscribe(topic, { qos }, (error) => {
        if (error) {
          console.log('Subscribe to topics error', error)
        } else {
          console.log('Subscribed to topic: ' + topic.toString())
        }
      });
    }
  };

  useEffect(() => {
    mqttConnect(getMQTTHost(), getMQTTConfig())
  }, []);

  useEffect(() => {
    if (client) {
      console.log(client)
      client.on('connect', () => {
        setConnectStatus('Connected');
        mqttSub({topic: "sensor/#", qos: 0})
        mqttSub({topic: "actor/#", qos: 0})
      });
      client.on('error', (err) => {
        console.error('Connection error: ', err);
        client.end();
      });
      client.on('reconnect', () => {
        setConnectStatus('Reconnecting');
      });
      client.on('disconnected', () => {
        console.warn('MQTTClient disconnected');
      });
      client.on('message', (topic, message) => {
        monitorRef.current?.onMessage(topic, message)
      });
    }
  }, [client]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="app">
      <div className={connectStatus === 'Connected' ? "connected" : "diconnected"}>
        <Monitor ref={monitorRef} />
      </div>
    </div>
  );
}
