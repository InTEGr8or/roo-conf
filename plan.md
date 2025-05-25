# Plan for Converting Bash Script to Python Package (roo-conf) and Adding Conversation Extraction

This document outlines the steps to convert a bash script that deploys configuration files into a Python package executable via `uvx roo-conf`, including new requirements for version management and command-line interface enhancements, automated publishing via GitHub Actions, the ability to pull prompt templates from a remote Git repository, componentized template deployment, editing source template files, synchronizing VS Code custom modes, and extracting conversations to Markdown.

## Objective

Create a Python package `roo-conf` that can be installed and executed using `uvx`. The package will deploy selected markdown files from either its package resources or a configured remote Git repository (pulled using a depth-1 clone) to a `.roo` directory in the current working directory, removing the `.md` extension and replacing a `{{repo-full-path}}` placeholder with the current repository path. The package will provide command-line interfaces for deploying (with component selection), editing source templates, configuring, pulling prompt templates, synchronizing VS Code custom modes, and extracting conversations to Markdown. Automated publishing to PyPI will be handled by a GitHub Actions workflow triggered by version changes.

## Current State

*   Initial Python package structure created using `uv init --package --lib`.
*   Existing files: `.gitignore`, `.python-version`, [`pyproject.toml`](pyproject.toml), [`README.md`](README.md), `src/`, [`src/roo_conf/__init__.py`](src/roo_conf/__init__.py), [`src/roo_conf/py.typed`](src/roo_conf/py.typed).
*   Markdown files (`system-prompt-architect-gh.md`, `system-prompt-code-gh.md`) are located in `src/roo_conf/prompts/`.
*   The original bash script (`transfer-to-repo.sh`) is located in `docs/source/roo/` for reference.
*   Documentation files (`README.md`, `plan.md`, `task.md`) are in the project root.
*   Initial Python deployment logic is in `src/roo_conf/deploy.py` with `deploy`, `edit`, and `config` subcommands.
*   `pyproject.toml` has the `[project.scripts]` entry point for `roo-conf`.
*   Automatic version incrementing script (`increment_version.py`) and a local build script (`publish.sh`) exist.
*   A GitHub Actions workflow file (`.github/workflows/workflow.yml`) has been created for automated publishing.
*   The remote template source feature has been implemented, allowing pulling templates from a Git repo to `~/.config/roo-conf/templates` using a depth-1 clone and re-clone for updates.
*   Componentized template deployment and refactoring of the edit command have been implemented.
*   The `sync-modes` command has been partially implemented, with logic for finding VS Code settings paths and synchronizing `custom_modes.yaml` files.

## Detailed Plan for Extracting Conversations to Markdown

This plan outlines the steps to add a new feature to `roo-conf` that extracts conversations related to a specific repository from VS Code and VS Code Insiders installations and saves them as Markdown files.

### Objective

Add a command to `roo-conf` that identifies conversations associated with a given repository in both VS Code and VS Code Insiders task history, extracts the conversation data, converts it to Markdown format, and saves the Markdown files within the repository's `.roo-conf/conversations/` subfolder.

### Detailed Plan

1.  **Add `extract-conversations` Subcommand:**
    *   Add a new subcommand `extract-conversations` to the `roo-conf` CLI using `argparse`.
    *   This subcommand will require an argument for the target repository path (defaulting to the current working directory).

2.  **Locate VS Code Global State Files:**
    *   Utilize the logic developed for the `sync-modes` command to find the global storage directories for both VS Code and VS Code Insiders (`~/.vscode-server[-insiders]/data/User/globalStorage/rooveterinaryinc.roo-cline/`).
    *   Determine the exact filename of the global state file within these directories that stores the "taskHistory". This may require inspecting the Roo-Code source code further or examining the contents of files in the global storage directory during implementation. Assume a conventional name like `globalState.json` for planning purposes, but be prepared to adjust.
    *   Construct the full paths to the global state files for both installations.

3.  **Read and Parse Task History:**
    *   For each identified global state file, read its content.
    *   Parse the file content (assuming it's JSON) to extract the data associated with the "taskHistory" key. This data is expected to be an array of `HistoryItem` objects.
    *   Implement error handling for file not found or parsing errors.

4.  **Filter Conversations by Repository:**
    *   Iterate through the array of `HistoryItem` objects obtained from the task history.
    *   For each `HistoryItem`, check if the `workspace` field exists and if its value matches the target repository path provided as a command argument.

5.  **Extract Conversation Data:**
    *   For each `HistoryItem` that matches the target repository:
        *   Construct the path to the corresponding task directory within the global storage (`<global_storage_path>/tasks/<task_id>/`).
        *   Construct the full paths to `api_conversation_history.json` and `ui_messages.json` within the task directory.
        *   Read the content of `api_conversation_history.json` and `ui_messages.json`.
        *   Implement error handling for file not found or parsing errors for these files.

6.  **Convert Conversation to Markdown:**
    *   Implement a function to convert the data from `api_conversation_history.json` and `ui_messages.json` into a single Markdown string.
    *   This conversion should format the conversation turns, including roles (user/assistant), message content, and potentially timestamps, in a readable Markdown format.

7.  **Save Conversations as Markdown Files:**
    *   Create a dedicated subfolder within the target repository to store the extracted conversations (e.g., `/home/mstouffer/repos/roo-conf/.roo-conf/conversations/`). Ensure this directory is created if it doesn't exist.
    *   For each converted Markdown conversation, generate a unique and descriptive filename (e.g., using the task ID, a timestamp, or a portion of the initial prompt).
    *   Write the Markdown content to a file with the generated filename within the `.roo-conf/conversations/` subfolder.
    *   Implement error handling for writing files.

8.  **Reporting:**
    *   Report the number of conversations found and extracted.
    *   Report any errors encountered during the process.

9.  **Documentation:**
    *   Update [`README.md`](README.md) to describe the new `extract-conversations` command, its purpose, arguments, and usage.

10. **Update Task List:**
    *   Update [`task.md`](task.md) to include the tasks for implementing the `extract-conversations` feature.

### Workflow Diagram

```mermaid
graph TD
    A[Start extract-conversations command] --> B{Get Target Repository Path};
    B --> C[Find VS Code Global Storage Directories];
    C --> D[Identify Global State File Paths];
    D --> E{Read & Parse Global State Files};
    E -- Success --> F[Extract Task History];
    E -- Error --> G[Report Error & End];
    F --> H{Filter History by Repository};
    H --> I{For Each Matching Conversation};
    I --> J[Construct Paths to Conversation Files];
    J --> K{Read Conversation Files};
    K -- Success --> L[Convert to Markdown];
    K -- Error --> M[Report Error & Continue/Skip];
    L --> N[Save Markdown File];
    N --> O[Report Success];
    M --> I;
    O --> I;
    I -- All Matches Processed --> P[Report Summary & End];
    G --> P;