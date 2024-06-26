/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";

import { memo } from "react";
import { NodeProps, NodeResizeControl } from "reactflow";
import { Container, Typography } from "@mui/material";
import { NodeData } from "../../stores/NodeData";
import SouthEastIcon from "@mui/icons-material/SouthEast";
import React from "react";
import { NodeHeader } from "../node/NodeHeader";
import OutputRenderer from "./OutputRenderer";
import useResultsStore from "../../stores/ResultsStore";
import { Position, Handle } from "reactflow";

const styles = (theme: any) =>
  css({
    "&": {
      display: "flex",
      flexDirection: "column",
      padding: 0,
      backgroundColor: theme.palette.c_gray2,
      width: "100%",
      height: "100%",
      minWidth: "150px",
      maxWidth: "1000px",
      minHeight: "150px",
      borderRadius: "2px"
    },
    "&.preview-node": {
      padding: 0,
      backgroundColor: "transparent",
      margin: 0,
      "&.collapsed": {
        maxHeight: "60px"
      },
      label: {
        display: "none"
      }
    },
    ".node-header": {
      width: "100%",
      height: "20px",
      minHeight: "unset",
      top: 0,
      left: 0,
      margin: 0,
      padding: 0,
      backgroundColor: theme.palette.c_gray1,
      border: 0
    },
    "& .react-flow__resize-control.handle.bottom.right": {
      opacity: 0,
      position: "absolute",
      right: "-8px",
      bottom: "-9px",
      transition: "opacity 0.2s"
    },
    "&:hover .react-flow__resize-control.handle.bottom.right": {
      opacity: 1
    },
    ".description": {
      position: "absolute",
      textAlign: "center",
      top: "50%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      zIndex: 0,
      fontFamily: theme.fontFamily2,
      width: "100%",
      color: theme.palette.c_gray5
    },
    // tabulator
    ".datatable.tabulator": {
      height: "calc(100% - 10px) !important",
      // height: "100%",
      maxHeight: "800px",
      overflowX: "scroll"
    },
    ".tabulator-editable": {
      cursor: "text",
      userSelect: "text"
    },
    ".table-actions": {
      padding: ".5em 0 0 .5em"
    },
    // tensor
    "& .tensor": {
      width: "100%",
      maxHeight: "500px",
      overflowY: "auto",
      padding: "1em"
    }
  });

interface PreviewNodeProps extends NodeProps<NodeData> { }

const PreviewNode: React.FC<PreviewNodeProps> = memo((props) => {
  const getResult = useResultsStore((state) => state.getResult);
  const result = getResult(props.data.workflow_id, props.id);

  return (
    <Container css={styles}>
      <Handle
        style={{ top: "50%" }}
        id="value"
        type="target"
        position={Position.Left}
        isConnectable={true}
      />
      <NodeResizeControl
        style={{ background: "red", border: "none" }}
        minWidth={150}
        minHeight={150}
        maxWidth={1000}
        maxHeight={1000}
      >
        <SouthEastIcon />
      </NodeResizeControl>
      <NodeHeader id={props.id} nodeTitle="Preview" isLoading={false} />

      {!result?.output && (
        <Typography className="description">Preview any output</Typography>
      )}
      <Handle
        style={{ top: "50%" }}
        id="value"
        type="target"
        position={Position.Left}
        isConnectable={true}
      />
      {result?.output && <OutputRenderer value={result?.output} />}
    </Container>
  );
});

PreviewNode.displayName = "PreviewNode";
export default PreviewNode;
