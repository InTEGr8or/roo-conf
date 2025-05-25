# Roo-Code Task and Workspace Relationship

This document details the relationship between tasks and workspaces in the Roo-Code VS Code extension, based on an investigation of the Roo-Code source code.

When the "Show tasks from all workspaces" option is enabled in the Roo-Code history view, the extension displays tasks associated with various workspaces. An examination of the `webview-ui/src/components/history/useTaskSearch.ts` file in the Roo-Code repository reveals how this relationship is managed.

The `useTaskSearch` React hook, responsible for filtering and displaying task history in the webview, accesses a `taskHistory` object and the current working directory (`cwd`), which represents the path of the currently open workspace.

The key finding is that each task history item (represented by the `HistoryItem` type/interface) includes an optional `workspace` field. When the "Show tasks from all workspaces" option is *not* selected, the `useTaskSearch` hook filters the `taskHistory` to include only those items where the `workspace` field matches the current `cwd`.

This confirms that the `workspace` field within the `HistoryItem` object is the mechanism used by Roo-Code to associate a task with a specific workspace.

The `HistoryItem` objects themselves are stored persistently within the VS Code global state, managed by the extension using the `ExtensionContext.globalState` API. This global state is likely stored in a file within the extension's global storage directory (`~/.vscode-server[-insiders]/data/User/globalStorage/rooveterinaryinc.roo-cline/`), although the exact filename and internal format of this storage require further investigation for direct access.

In summary, the relationship between a Roo-Code task and its associated workspace is explicitly stored in the `workspace` field of the `HistoryItem` object within the VS Code global state. This allows the extension to filter and display tasks relevant to the current workspace.