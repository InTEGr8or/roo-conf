# Implementation Task List for roo-conf

This file outlines the tasks for implementing new features and fixes in the `roo-conf` package.

## Modify Roo-Code to Auto-Export Conversations:

- Identify the code within the Roo-Code repository that handles the completion of a task (likely related to `RooCodeEventName.TaskCompleted` in `ClineProvider.ts` or `src/exports/api.ts`).
- At the task completion trigger point, access the completed task's data, including the `HistoryItem` and conversation content (`api_conversation_history.json` and `ui_messages.json`).
- Get the workspace path from the `HistoryItem`.
- Construct the target directory path for the exported conversation within the workspace (e.g., `.roo-convo/`).
- Construct the full file path for the Markdown export within the `.roo-convo/` directory, using a descriptive filename.
- Implement or adapt the logic to convert the conversation data into a single Markdown string.
- Use VS Code's file system API (`vscode.workspace.fs.writeFile`) or Node.js `fs` module to create the `.roo-convo/` directory (if it doesn't exist) and write the Markdown content to the target file path.
- Consider adding a configuration option in Roo-Code's settings to enable/disable this auto-export feature and potentially configure the export directory name.
- Implement error handling for file system operations.
- Add or modify tests in the Roo-Code test suite to cover the new auto-export functionality.
- Update the Roo-Code documentation to describe the new auto-export feature.

## Investigations Completed:

- Investigated how Roo-Code relates conversations to workspaces by examining `webview-ui/src/components/history/useTaskSearch.ts`. Confirmed that the `workspace` field in the `HistoryItem` object is used for this relationship. Documented this finding in `docs/roo-code_task_workspace_relationship.md`.

## Summary of Progress and Next Steps:

The investigation into the task-workspace relationship is complete and documented. The focus has shifted from building an extraction tool in `roo-conf` to modifying the Roo-Code extension itself to automatically export conversations upon task completion. The tasks for implementing this modification in the Roo-Code repository are outlined above.

## Achievements:

- Restored missing command-line arguments (`deploy`, `edit`, `config`, `pull`, `sync-modes`) in the `roo-conf` CLI by modifying `src/roo_conf/__init__.py` to include subparsers defined in `src/roo_conf/deploy.py`.
- Updated `publish.sh` to include a step (`uv run python increment_version.py`) to automatically increment the patch version before building and publishing the package.