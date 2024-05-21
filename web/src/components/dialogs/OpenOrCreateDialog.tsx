/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";

import { useCallback } from "react";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import Button from "@mui/material/Button";
import { useQuery, useQueryClient } from "react-query";
import { useWorkflowStore } from "../../stores/WorkflowStore";
import { Workflow, WorkflowList } from "../../stores/ApiTypes";
import {
  Box,
  CircularProgress,
  ToggleButton,
  ToggleButtonGroup,
  Typography
} from "@mui/material";
import { ErrorOutlineRounded } from "@mui/icons-material";
import { prettyDate } from "../../utils/formatDateAndTime";
import { truncateString } from "../../utils/truncateString";
import { useNavigate } from "react-router";
import { useNodeStore } from "../../stores/NodeStore";
import { useSettingsStore } from "../../stores/SettingsStore";
import ThemeNodetool from "../themes/ThemeNodetool";

const styles = (theme: any) =>
  css({
    ".MuiBackdrop-root": { background: "transparent" },
    ".MuiPaper-root": {
      width: "70vw",
      height: "70vh",
      maxWidth: "1000px",
      maxHeight: "800px",
      padding: "2em",
      display: "flex",
      flexDirection: "column",
      gap: "1em",
      transition: "all .6s",
      background: theme.palette.c_gray1
    },
    ".title": {
      position: "absolute",
      left: "2em",
      color: theme.palette.c_white,
      fontSize: theme.fontSizeBigger,
      margin: "0",
      textAlign: "center"
    },
    ".recent-hl": {
      color: theme.palette.c_gray6,
      textTransform: "uppercase",
      fontFamily: theme.fontFamily1
    },
    ".toggle-name-date": {
      marginLeft: "auto",
      paddingRight: "3em",
      height: "1.5em"
    },
    ".content": {
      position: "relative",
      display: "flex",
      flexDirection: "column",
      alignItems: "flex-start",
      gap: "1em",
      margin: "0",
      padding: "0",

      overflow: "hidden"
    },
    ".recent": {
      position: "relative",
      display: "flex",
      flexDirection: "column",
      flexGrow: 1,
      gap: "1em",
      height: "75%",
      width: "100%"
    },
    ".recent .tools": {
      position: "relative",
      display: "flex",
      flexDirection: "row",
      gap: "1em",
      marginTop: "2em"
    },
    ".recent h4": { margin: "0" },
    ".recent .items": { height: "100%", position: "relative" },
    ".workflow-buttons": {
      display: "flex",
      flexDirection: "row",
      gap: "1em",
      justifyContent: "center",
      marginLeft: "6em",
      alignItems: "center"
    }
  });

const listStyles = () =>
  css({
    "&": {
      display: "flex",
      flexDirection: "column",
      alignItems: "flex-start",
      margin: "0",
      padding: "0 0 2em 0",
      height: "90%",
      overflow: "hidden auto"
    },
    ".workflow": {
      position: "relative",
      display: "flex",
      flexDirection: "row",
      gap: "1em",
      alignItems: "flex-start",
      margin: ".25em 0",
      padding: "0.4em .5em",
      width: "calc(100% - 20px)",
      cursor: "pointer",
      borderBottom: "1px solid black",
      backgroundColor: ThemeNodetool.palette.c_gray1,
      transition: "background-color 0.2s ease-in-out"
    },
    ".workflow:hover": {
      backgroundColor: ThemeNodetool.palette.c_gray2,
      outline: `0`
    },
    ".name-and-description": {
      display: "flex",
      flexDirection: "column",
      gap: "0.1em"
    },
    ".name": {
      fontSize: ThemeNodetool.fontSizeNormal,
      wordSpacing: "-3px",
      margin: "0",
      lineHeight: "1em",
      color: ThemeNodetool.palette.c_hl1
    },
    ".description": {
      margin: "0.1em 0 .1em"
    },
    ".date": {
      marginLeft: "auto",
      paddingRight: "1em",
      fontFamily: ThemeNodetool.fontFamily2,
      right: "0",
      minWidth: "150px"
    },
    ".image-wrapper": {
      flexShrink: 0,
      width: "40px",
      height: "40px",
      overflow: "hidden",
      position: "relative",
      backgroundColor: ThemeNodetool.palette.c_gray3
    },
    ".right": {
      display: "flex",
      alignItems: "center",
      minWidth: "200px",
      marginLeft: "auto"
    },
    ".right button": {}
  });

const OpenOrCreateDialog = () => {
  const settings = useSettingsStore((state) => state.settings);
  const loadWorkflows = useWorkflowStore((state) => state.load);
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const createNewWorkflow = useWorkflowStore((state) => state.createNew);
  const setWorkflowOrder = useSettingsStore((state) => state.setWorkflowOrder);
  const setShouldAutoLayout = useNodeStore(
    (state) => state.setShouldAutoLayout
  );

  function addBreaks(text: string) {
    return text.replace(/([-_.])/g, "$1<wbr>");
  }
  // LOAD WORKFLOWS
  const { data, isLoading, error, isError } = useQuery<WorkflowList, Error>(
    ["workflows"],
    async () => {
      return loadWorkflows("");
    },
    {
      useErrorBoundary: true
    }
  );

  // CREATE NEW WORKFLOW
  const handleCreateNewWorkflow = async () => {
    const workflow = await createNewWorkflow();
    queryClient.invalidateQueries(["workflows"]);
    navigate(`/editor/${workflow.id}`);
  };

  // BROWSE WORKFLOWS
  const handleNavigateUserWorkflows = () => {
    navigate("/workflows");
  };
  const handleNavigateExampleWorkflows = () => {
    navigate("/workflows?category=examples");
    // navigate("/workflows");
  };

  const onClickWorkflow = useCallback(
    (workflow: Workflow) => {
      // setShouldAutoLayout(true);
      navigate("/editor/" + workflow.id);
    },
    [navigate]
  );

  // ORDER
  const handleOrderChange = (_: any, newOrder: any) => {
    if (newOrder !== null) {
      setWorkflowOrder(newOrder);
    }
  };

  const sortedWorkflows = data?.workflows.sort((a, b) => {
    if (settings.workflowOrder === "name") {
      return a.name.localeCompare(b.name);
    }
    return b.updated_at.localeCompare(a.updated_at);
  });

  // (a, b) =>
  //   new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
  // List view
  const renderListView = (workflows: any) => (
    <Box className="container list" css={listStyles}>
      {workflows.map((workflow: Workflow) => (
        <Box
          key={workflow.id}
          className="workflow list"
          onClick={() => onClickWorkflow(workflow)}
        >
          <Box
            className="image-wrapper"
            sx={{
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundImage: workflow.thumbnail_url
                ? `url(${workflow.thumbnail_url})`
                : "none",
              width: "50px",
              height: "50px"
            }}
          >
            {!workflow.thumbnail_url && <Box className="image-placeholder" />}
          </Box>
          <Box className="name-and-description">
            <div
              className="name"
              dangerouslySetInnerHTML={{ __html: addBreaks(workflow.name) }}
            ></div>
            <Typography className="description">
              {truncateString(workflow.description, 350)}
            </Typography>
          </Box>
          <div className="right">
            <Typography className="date">
              {prettyDate(workflow.updated_at, "verbose", settings)}
            </Typography>
          </div>
        </Box>
      ))}
    </Box>
  );
  return (
    <Dialog
      css={styles}
      open={true}
      components={{
        Backdrop: () => null
      }}
      style={{ top: "100px" }}
    >
      <Typography className="title" variant="h4">
        NODE
        <br />
        TOOL
      </Typography>
      <DialogContent className="content">
        <div className="workflow-buttons">
          <Button variant="outlined" onClick={handleCreateNewWorkflow}>
            Create New
          </Button>
          <Button color="primary" onClick={handleNavigateUserWorkflows}>
            My Workflows
          </Button>
          <Button color="primary" onClick={handleNavigateExampleWorkflows}>
            Examples
          </Button>
        </div>

        <div className="recent">
          <div className="tools">
            <Typography className="recent-hl">Recent Workflows</Typography>
            <ToggleButtonGroup
              className="toggle-name-date"
              value={settings.workflowOrder}
              onChange={handleOrderChange}
              exclusive
              aria-label="Sort workflows"
            >
              <ToggleButton value="name" aria-label="Sort by name">
                Name
              </ToggleButton>
              <ToggleButton value="updated_at" aria-label="sort by date">
                Date
              </ToggleButton>
            </ToggleButtonGroup>
          </div>
          <div className="items">
            {isLoading && <CircularProgress />}
            {isError && (
              <ErrorOutlineRounded>
                ERROR
                <Typography>{error?.message}</Typography>
              </ErrorOutlineRounded>
            )}
            {data && renderListView(sortedWorkflows)}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default OpenOrCreateDialog;
