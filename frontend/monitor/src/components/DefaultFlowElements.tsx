import  { Background, Controls, MiniMap, Node } from 'react-flow-renderer';

export default function DefaultFlowElements() {
    return (
        <>
            <MiniMap
                nodeStrokeColor={(n: Node): string => {
                    if (n.style?.background) return n.style.background.toString();
                    if (n.type === 'input') return '#0041d0';
                    if (n.type === 'output') return '#ff0072';
                    if (n.type === 'default') return '#1a192b';
                    return '#eee';
                }}
                nodeColor={(n: Node): string => {
                    if (n.style?.background) return n.style.background.toString();
                    return '#fff';
                }}
                nodeBorderRadius={2}
            />
            <Controls />
            <Background color="#aaa" gap={16} />
        </>
    );
}