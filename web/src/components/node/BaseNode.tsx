/** @jsxImportSource @emotion/react */
import { memo } from "react";
import { NodeProps } from "reactflow";
import { isEqual } from "lodash";
import { Container } from "@mui/material";
import { NodeData } from "../../stores/NodeData";
import { useMetadata } from "../../serverState/useMetadata";

import { useNodeStore } from "../../stores/NodeStore";
import useResultsStore from "../../stores/ResultsStore";
import OutputRenderer from "./OutputRenderer";
import { NodeHeader } from "./NodeHeader";
import { NodeFooter } from "./NodeFooter";
import { NodeInputs } from "./NodeInputs";
import { NodeOutputs } from "./NodeOutputs";
import { NodeLogs } from "./NodeLogs";
import { ProcessTimer } from "./ProcessTimer";
import { NodeProgress } from "./NodeProgress";
import { NodeErrors } from "./NodeErrors";
import useStatusStore from "../../stores/StatusStore";

export const TOOLTIP_ENTER_DELAY = 650;
export const TOOLTIP_LEAVE_DELAY = 200;
export const TOOLTIP_ENTER_NEXT_DELAY = 350;
/**
 * Split a camelCase string into a space separated string.
 */
function capitalToSpace(str: string) {
  const s = str.replace(/([A-Z]+)([A-Z][a-z])/g, "$1 $2");
  return s.replace(/([a-z])([A-Z])/g, "$1 $2");
}


function isSmallNode(type: string) {
  return type.match(/\.math|\.tensor|\.list|\.dictionary/) !== null;
}

/**
 * BaseNode renders a single node in the workflow
 *
 * @param props
 */

export default memo(
  function BaseNode(props: NodeProps<NodeData>) {
    const {
      data: metadata,
      isLoading: metadataLoading,
      error: metadataError
    } = useMetadata();
    const nodedata = useNodeStore((state) => state.findNode(props.id)?.data);
    const workflowId = nodedata?.workflow_id;
    const status = useStatusStore((state) =>
      workflowId !== undefined
        ? state.getStatus(workflowId, props.id)
        : undefined
    );
    const getInputEdges = useNodeStore((state) => state.getInputEdges);
    const getResult = useResultsStore((state) => state.getResult);
    const result = getResult(props.data.workflow_id, props.id);
    const edges = getInputEdges(props.id);
    const isLoading =
      status === "running" || status === "starting" || status === "processing";
    const isConstantNode = props.type.startsWith("nodetool.constant");
    const isInputNode = props.type.startsWith("nodetool.input");
    const isOutputNode =
      props.type.startsWith("nodetool.output") ||
      props.type === "comfy.image.SaveImage";
    const className = `node-body ${props.data.collapsed ? "collapsed" : ""}
      ${isInputNode ? " input-node" : ""} ${isOutputNode ? " output-node" : ""}
      ${props.data.dirty ? "dirty" : ""}`
      .replace(/\s+/g, " ")
      .trim();

    const nodeStyle = isSmallNode(props.type) ? 'small' : 'normal';

    if (!metadata) {
      return (
        <Container className={className}>
          {metadataLoading && <span>Loading...</span>}
          {metadataError !== undefined && (
            <span>{metadataError?.toString()}</span>
          )}
        </Container>
      );
    }

    const nodeMetadata = metadata.metadataByType[props.type];

    const node_title = capitalToSpace(nodeMetadata.title || "");
    const node_namespace = nodeMetadata.namespace || "";
    const firstOutput =
      nodeMetadata.outputs.length > 0
        ? nodeMetadata.outputs[0]
        : {
          name: "output",
          type: {
            type: "string"
          }
        };

    return (
      <Container className={className}>
        <>
          <NodeHeader
            id={props.id}
            nodeTitle={node_title}
            isLoading={isLoading}
          />
          <div className="node-content-hidden" />
          <NodeErrors id={props.id} />
        </>
        <NodeOutputs id={props.id} outputs={nodeMetadata.outputs} />
        <NodeInputs
          id={props.id}
          nodeStyle={nodeStyle}
          properties={nodeMetadata.properties}
          data={props.data}
          isConstantNode={isConstantNode}
          edges={edges}
        />

        {isOutputNode && (
          <div className="node-output">
            {nodeMetadata.outputs.map((output) => (
              <div key={output.name}>
                <OutputRenderer
                  value={result ? result[output.name] : null}
                  type={output.type}
                />
              </div>
            ))}
          </div>
        )}
        {nodeStyle === 'normal' && (
          <>
            <ProcessTimer isLoading={isLoading} status={status} />
            <NodeProgress id={props.id} />

            <NodeFooter
              nodeNamespace={node_namespace}
              type={firstOutput.type.type}
            />
            <NodeLogs id={props.id} />
          </>
        )}
      </Container >
    );
  },
  (prevProps, nextProps) => isEqual(prevProps, nextProps)
);
