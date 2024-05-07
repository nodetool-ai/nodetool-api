import { create } from "zustand";
import { authHeader, client } from "./ApiClient";
import { Workflow, WorkflowList, WorkflowRequest } from "./ApiTypes";
import { uuidv4 } from "./uuidv4";
import { QueryClient, QueryKey } from "react-query";

export interface WorkflowStore {
  shouldFitToScreen: boolean;
  setShouldFitToScreen: (shouldFitToScreen: boolean) => void;
  invalidateQueries: (queryKey: QueryKey) => void;
  queryClient: QueryClient | null;
  setQueryClient: (queryClient: QueryClient) => void;
  newWorkflow: () => Workflow;
  add: (workflow: Workflow) => void;
  getFromCache: (id: string) => Workflow | undefined;
  create: (workflow: WorkflowRequest) => Promise<Workflow>;
  createNew: () => Promise<Workflow>;
  load: (cursor?: string, limit?: number) => Promise<WorkflowList>;
  loadIDs: (ids: string[]) => Promise<Workflow[]>;
  loadPublic: (cursor?: string) => Promise<WorkflowList>;
  loadExamples: () => Promise<WorkflowList>;
  get: (id: string) => Promise<Workflow | undefined>;
  copy: (workflow: Workflow) => Promise<Workflow>;
  update: (workflow: Workflow) => Promise<Workflow>;
  delete: (id: string) => Promise<void>;
}

const sortWorkflows = (workflows: Workflow[]) =>
  workflows.sort((a: Workflow, b: Workflow) => {
    if (a.created_at && b.created_at) {
      return a.created_at.localeCompare(b.created_at);
    }
    if (!a.created_at) {
      return -1; // Treat 'a' as earlier if 'created_at' is undefined
    }
    return 1; // Treat 'b' as earlier if 'a.created_at' is defined but 'b.created_at' is not
  });

export const useWorkflowStore = create<WorkflowStore>((set, get) => ({
  shouldFitToScreen: false,

  /**
   * Set whether the graph should fit to the screen.
   */
  setShouldFitToScreen: (shouldFitToScreen: boolean) => {
    set({ shouldFitToScreen });
  },

  queryClient: null,

  /**
   * Set the react query client to allow changing/clearing the cache.
   */
  setQueryClient: (queryClient: QueryClient) => {
    set({ queryClient });
  },

  /**
   * Clear the cache for a given query.
   */
  invalidateQueries: (queryKey: QueryKey) => {
    get().queryClient?.invalidateQueries(queryKey);
  },

  /**
   * Add a workflow to the cache.
   */
  add: (workflow: Workflow) => {
    get().queryClient?.setQueryData(["workflows", workflow.id], workflow);
  },

  /**
   * Get a workflow from the cache.
   * Should only be used outside of react context.
   */
  getFromCache: (id: string) => {
    return get().queryClient?.getQueryData(["workflows", id]);
  },

  /**
   * Create a new workflow.
   */
  newWorkflow: () => {
    const data = {
      id: "",
      name: "New Workflow",
      description: "",
      access: "private",
      thumbnail: "",
      updated_at: new Date().toISOString(),
      created_at: new Date().toISOString(),
      graph: {
        nodes: [],
        edges: []
      }
    };
    get().add(data);
    return data;
  },

  /**
   * Create new workflow.
   */
  createNew: async () => {
    return await get().create(get().newWorkflow());
  },

  /**
   * Create a workflow on the server.
   *
   * @param workflow The workflow to add.
   */
  create: async (workflow: WorkflowRequest) => {
    const { data, error } = await client.POST("/api/workflows/", {
      params: { header: authHeader() },
      body: workflow
    });
    if (error) {
      throw error;
    }
    get().invalidateQueries(["workflows"]);
    return data;
  },

  /**
   * Get a list of workflows from the server.
   */
  load: async (cursor?: string, limit?: number) => {
    cursor = cursor || "";
    const { data, error } = await client.GET("/api/workflows/", {
      params: { query: { cursor, limit }, header: authHeader() }
    });
    if (error) {
      throw error;
    }
    for (const workflow of data.workflows) {
      get().add(workflow);
    }
    return data;
  },

  /**
   * Load IDs of workflows from the server.
   */
  loadIDs: async (workflowIds: string[]) => {
    const getWorkflow = get().get;
    const promises = workflowIds.map((id) => getWorkflow(id));
    const workflows = await Promise.all(promises);
    for (const workflow of workflows) {
      if (workflow) {
        get().add(workflow);
      }
    }
    return workflows.filter((w) => w !== undefined) as Workflow[];
  },

  /**
   * Get a list of public workflows from the server.
   */
  loadPublic: async (cursor?: string) => {
    cursor = cursor || "";
    const { data, error } = await client.GET("/api/workflows/public", {
      params: { query: { cursor } }
    });
    if (error) {
      throw error;
    }
    return data;
  },

  /**
   * Load example workflows from the server.
   */
  loadExamples: async () => {
    const { data, error } = await client.GET("/api/workflows/examples", {});
    if (error) {
      throw error;
    }
    return data;
  },

  /**
   * Get a workflow from the store or load it from the server.
   *
   * @param id The id of the workflow to get.
   */
  get: async (id: string) => {
    const { data, error } = await client.GET("/api/workflows/{id}", {
      params: { path: { id }, header: authHeader() }
    });
    if (error) {
      throw error;
    }
    return data;
  },

  /**
   * Update a workflow on the server.
   *
   * @param workflow The workflow to update.
   * @returns A promise that resolves when the workflow is updated.
   */
  update: async (workflow: Workflow) => {
    if (workflow.id === "") {
      console.warn("Cannot update workflow with empty ID");
      return workflow;
    }
    const { error, data } = await client.PUT("/api/workflows/{id}", {
      params: {
        path: { id: workflow.id },
        header: authHeader()
      },
      body: workflow
    });
    if (error) {
      throw error;
    }
    get().add(data);
    return data;
  },

  /**
   * Copy a workflow.
   */
  copy: async (workflow: Workflow) => {
    return await get().create({
      name: workflow.name,
      description: workflow.description,
      thumbnail: workflow.thumbnail,
      access: "private",
      graph: workflow.graph
    });
  },

  /**
   * Delete a workflow from the store and the server.
   *
   * @param id The ID of the workflow to delete.
   * @returns A promise that resolves when the workflow is deleted.
   */
  delete: async (id: string) => {
    const { error, data } = await client.DELETE("/api/workflows/{id}", {
      params: { path: { id }, header: authHeader() }
    });
    if (error) {
      throw error;
    }
    get().invalidateQueries(["workflows"]);
  }
}));