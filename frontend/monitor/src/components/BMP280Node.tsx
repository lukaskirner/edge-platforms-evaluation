import React, { memo } from 'react';
import './CustomNode.scss'
import { Handle, Position, Node } from 'react-flow-renderer';

export interface BMP280NodeData {
  label: string,
  temperature: number,
  pressure: number,
  altitude: number
}

export default memo<Node<BMP280NodeData>>((node) => {
  return (
    <>
      <Handle
        type="source"
        position={Position.Top}
        style={{ background: '#555' }}
      />
      <div className="react-flow__node-default costum-node">
        <strong>{node.data?.label}</strong>
        <p>{node.data?.temperature} °C</p>
        <p>{node.data?.pressure} hpa</p>
        <p>{node.data?.altitude} m</p>
      </div>
    </>
  );
});
