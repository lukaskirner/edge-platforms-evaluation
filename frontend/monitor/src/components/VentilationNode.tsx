import React, { memo } from 'react';
import './CustomNode.scss'
import { Handle, Position, Node } from 'react-flow-renderer';

export interface VentilationData {
  label: string
}

export default memo<Node<VentilationData>>((node) => {
  return (
    <>
      <Handle
        type="source"
        position={Position.Top}
        style={{ background: '#555' }}
      />
      <div className="react-flow__node-default costum-node">
        <strong>{node.data?.label}</strong>
        <p>State: </p>
        <br />
        <button> Toggle </button>
      </div>
    </>
  );
});
