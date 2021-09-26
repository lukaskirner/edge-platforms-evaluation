import React, { useEffect, useImperativeHandle, useState } from 'react';
import './Monitor.scss'
import ReactFlow, { Elements } from 'react-flow-renderer';
import DefaultFlowElements from '../../components/DefaultFlowElements';
import { getReactFlowElements } from '../../core/MonitorApiClient';
import BMP280Node from '../../components/BMP280Node';
import MQ2Node from '../../components/MQ2Node';
import VentilationNode from '../../components/VentilationNode';

const initialElements: Elements = [];

export type MonitorProps = {}

export type MonitorHandle = {
  onMessage: (topic: string, message: Buffer) => void,
}

const nodeTypes = {
  bmp280Node: BMP280Node,
  mq2Node: MQ2Node,
  ventilationNode: VentilationNode
};

const Monitor: React.ForwardRefRenderFunction<MonitorHandle, MonitorProps> = (props, ref) => {
  const [elements, setElements] = useState<Elements>(initialElements);
  
  useEffect(() => {
    (async () => {
      let elem = await getReactFlowElements()
      if (elem != null) { setElements(elem!) }
    })()
  }, []);

  useImperativeHandle(ref, () => ({
    onMessage(topic: string, message: Buffer) {
      let id = topic.replaceAll("/", "-")
      setElements((els) => {
        return els.map((el) => {
          if (el.id === id) {
            if (topic.startsWith("sensor/bmp280/") || topic.startsWith("sensor/mq2/")) {
              let data = JSON.parse(message.toString())
              el.data = {
                ...el.data,
                ...data
              }
            }
          }

          return el
        })
      })
    }
  }));

  return (
    <div className="monitor">
      <ReactFlow 
          elements={elements}
          nodeTypes={nodeTypes}
          snapToGrid={true}
          snapGrid={[15, 15]}>

          <DefaultFlowElements />
      </ReactFlow>
    </div>
  );
}

export default React.forwardRef(Monitor);
