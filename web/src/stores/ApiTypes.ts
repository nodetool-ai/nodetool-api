import { components } from "../api";

export type User = components["schemas"]["User"];
export type Node = components["schemas"]["Node"];
export type Edge = components["schemas"]["Edge"];
export type Asset = components["schemas"]["Asset"];
export type AssetList = components["schemas"]["AssetList"];
export type AssetRef = components["schemas"]["AssetRef"];
export type AssetUpdateRequest = components["schemas"]["AssetUpdateRequest"];
export type ImageRef = components["schemas"]["ImageRef"];
export type DataframeRef = components["schemas"]["DataframeRef"];
export type ColumnDef = components["schemas"]["ColumnDef"];
export type AudioRef = components["schemas"]["AudioRef"];
export type VideoRef = components["schemas"]["VideoRef"];
export type Tensor = components["schemas"]["Tensor"];
export type TextRef = components["schemas"]["TextRef"];
export type FileRef = components["schemas"]["FileRef"];
export type WorkflowRef = components["schemas"]["WorkflowRef"];
export type NodeRef = components["schemas"]["NodeRef"];
export type Workflow = components["schemas"]["Workflow"];
export type WorkflowList = components["schemas"]["WorkflowList"];
export type WorkflowRequest = components["schemas"]["WorkflowRequest"];
export type Property = components["schemas"]["Property"];
export type OutputSlot = components["schemas"]["OutputSlot"];
export type NodeMetadata = components["schemas"]["NodeMetadata"];
export type TypeMetadata = components["schemas"]["TypeMetadata"];
export type ThreadMessage = components["schemas"]["ThreadMessage"];
export type Thread = components["schemas"]["Thread"];
export type Prediction = components["schemas"]["Prediction"];
export type MessageList = components["schemas"]["MessageList"];
export type MessageTextContent = components["schemas"]["MessageTextContent"];
export type MessageImageContent = components["schemas"]["MessageImageContent"];
export type OAuthAuthorizeRequest =
  components["schemas"]["OAuthAuthorizeRequest"];
export type Image = components["schemas"]["ImageRef"];
export type FolderRef = components["schemas"]["FolderRef"];
export type Audio = components["schemas"]["AudioRef"];
export type Video = components["schemas"]["VideoRef"];
export type RunJobRequest = components["schemas"]["RunJobRequest"];
export type NodeUpdate = components["schemas"]["NodeUpdate"];
export type NodeProgress = components["schemas"]["NodeProgress"];
export type JobUpdate = components["schemas"]["JobUpdate"];
export type WorkflowUpdate = components["schemas"]["WorkflowUpdate"];

// a type that allows arbitrary members
export type TypeName = string;
export type WorkflowAttributes = Omit<Workflow, "graph">;
