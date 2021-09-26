import React, { memo } from 'react';
import './CustomNode.scss'
import { Handle, Position, Node } from 'react-flow-renderer';

export interface MQ2NodeData {
  label: string,
  isGas: boolean,
  gasVal: number
}

export default memo<Node<MQ2NodeData>>((node) => {
  return (
    <>
      <Handle
        type="source"
        position={Position.Top}
        style={{ background: '#555' }}
      />
      <div className="react-flow__node-default costum-node">
        <strong>{node.data?.label}</strong>
        <p>Is gas: {node.data?.isGas}</p>
        <p>{node.data?.gasVal} %</p>
      </div>
    </>
  );
});
