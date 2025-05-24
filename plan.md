# Plan for Converting Bash Script to Python Package (roo-conf)

This document outlines the steps to convert a bash script that deploys configuration files into a Python package executable via `uvx roo-conf`, including new requirements for version management and command-line interface enhancements, automated publishing via GitHub Actions, the ability to pull prompt templates from a remote Git repository, componentized template deployment, editing source template files, and synchronizing VS Code custom modes.

## Objective

Create a Python package `roo-conf` that can be installed and executed using `uvx`. The package will deploy selected markdown files from either its package resources or a configured remote Git repository (pulled using a depth-1 clone) to a `.roo` directory in the current working directory, removing the `.md` extension and replacing a `{{repo-full-path}}` placeholder with the current repository path. The package will provide command-line interfaces for deploying (with component selection), editing source templates, configuring, pulling prompt templates, and synchronizing VS Code custom modes. Automated publishing to PyPI will be handled by a GitHub Actions workflow triggered by version changes.

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

## Detailed Plan

1.  **Add `sync-modes` Subcommand:**
    *   Modify [`src/roo_conf/deploy.py`](src/roo_conf/deploy.py) (or create a new file like `src/roo_conf/sync.py` and register it) to include a new subcommand `sync-modes` using `argparse`.
    *   This subcommand will not require any arguments initially.

2.  **Locate `custom_modes.yaml` Files (POSIX):**
    *   Implement a function (e.g., `find_vscode_settings_paths`) that determines the potential paths to the `settings` directories for VS Code and VS Code Insiders on POSIX.
    *   This function will use the user's home directory path (available from the environment) and the conventional relative paths:
        *   VS Code Insiders: `~/.vscode-server-insiders/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/custom_modes.yaml`
        *   VS Code: `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/custom_modes.yaml`
    *   Construct the full paths to the `custom_modes.yaml` files using these conventions.
    *   Verify the existence of these files. If a file is not found, report an error or warning but continue if the other file exists.

3.  **Determine Latest Version:**
    *   For each existing `custom_modes.yaml` file found, get the last modified timestamp.
    *   Compare the timestamps to identify the most recently modified file.
    *   If only one file exists, that is considered the latest version.

4.  **Synchronize Files:**
    *   Read the content of the latest `custom_modes.yaml` file.
    *   Copy the content of the latest file to the other location(s) where the `custom_modes.yaml` file exists.
    *   Use Python's file I/O operations for reading and writing. Ensure necessary directories are created if they don't exist (though the settings directories should exist if VS Code is installed).

5.  **Error Handling and Reporting:**
    *   Include error handling for cases where files or directories are not found.
    *   Report which file was considered the latest and where it was copied.
    *   Report any errors encountered during the process.

6.  **Modularity for Windows Extension:**
    *   Structure the code for finding the paths (Step 2) in a way that can be easily extended for different operating systems. This might involve an OS-checking mechanism and separate functions for finding paths on POSIX and Windows.
    *   The core synchronization logic (Steps 3 and 4) should be OS-agnostic, operating on the determined file paths.

7.  **Integration:**
    *   Add the new `sync-modes` subcommand to the main `roo-conf` entry point in [`pyproject.toml`](pyproject.toml) and the CLI parsing logic in `src/roo_conf/deploy.py` (or the new sync file).

### Future Considerations (Windows Support)

*   Investigate methods for finding VS Code installation paths on Windows. This might involve:
    *   Checking environment variables (e.g., `VSCODE_CWD`).
    *   Querying the Windows Registry.
    *   Searching in known installation locations (e.g., `%APPDATA%\Code\User\`, `%APPDATA%\Code - Insiders\User\`).
*   Implement a Windows-specific version of the `find_vscode_settings_paths` function.

### Workflow Diagram

```mermaid
graph TD
    A[Start sync-modes command] --> B{Determine OS};
    B -- POSIX --> C[Find VS Code Settings Paths POSIX Convention];
    B -- Windows (Future) --> D[Find VS Code Settings Paths Windows Logic];
    C --> E{Verify File Existence};
    D --> E;
    E -- Files Found --> F[Determine Latest custom_modes.yaml];
    E -- No Files Found --> G[Report Error/Warning];
    F --> H[Read Latest File Content];
    H --> I[Copy Content to Other Locations];
    I --> J[Report Success];
    G --> K[End Task];
    J --> K;