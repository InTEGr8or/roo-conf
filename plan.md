# Plan for Converting Bash Script to Python Package (roo-conf)

This document outlines the steps to convert a bash script that deploys configuration files into a Python package executable via `uvx roo-conf`, including new requirements for version management and command-line interface enhancements.

## Objective

Create a Python package `roo-conf` that can be installed and executed using `uvx`. The package will deploy markdown files stored within it to a `.roo` directory in the current working directory, removing the `.md` extension and replacing a `{{repo-full-path}}` placeholder with the current repository path. Additionally, the package will support automatic version incrementing upon publishing and provide a command-line interface for listing or indicating specific deployed files.

## Current State

*   Initial Python package structure created using `uv init --package --lib`.
*   Existing files: `.gitignore`, `.python-version`, [`pyproject.toml`](pyproject.toml), [`README.md`](README.md), `src/`, [`src/roo_conf/__init__.py`](src/roo_conf/__init__.py), [`src/roo_conf/py.typed`](src/roo_conf/py.typed).
*   Markdown files (`system-prompt-architect-gh.md`, `system-prompt-code-gh.md`) are located in `src/roo_conf/prompts/`.
*   The original bash script (`transfer-to-repo.sh`) is located in `docs/source/roo/` for reference.
*   Documentation files (`README.md`, `plan.md`, `task.md`) have been created/updated in the project root.
*   Initial Python deployment logic is in `src/roo_conf/deploy.py`.
*   `pyproject.toml` has the `[project.scripts]` entry point for `roo-conf`.

## Detailed Plan

1.  **Project Structure:**
    *   The markdown files are located in `src/roo_conf/prompts/`.
    *   The bash script [`transfer-to-repo.sh`](docs/source/roo/transfer-to-repo.sh) is kept in `docs/source/roo/` for reference.
    *   Documentation files (`README.md`, `plan.md`, `task.md`) are in the project root.

2.  **Python Implementation (`src/roo_conf/deploy.py`):**
    *   Refactor `src/roo_conf/deploy.py` to use a command-line argument parser (e.g., `argparse`).
    *   Add an argument (e.g., `--file` or `-f`) to specify a deployed file name (without the `.md` extension).
    *   If no file argument is provided, list the available deployed file names (derived from the files in `src/roo_conf/prompts/`, without the `.md` extension).
    *   If a file argument is provided, indicate the path to the corresponding deployed file in the `.roo` directory. (Future enhancement could be to open the file for editing).
    *   Keep the existing deployment logic as the default behavior when no specific file action is requested.

3.  **`pyproject.toml` Update:**
    *   Ensure the `[project.scripts]` section correctly points to the entry point in `src/roo_conf/deploy.py`.

4.  **Documentation Files:**
    *   Update [`README.md`](README.md) to include instructions for the new command-line options (`--file` and listing files).
    *   Update [`task.md`](task.md) to track the progress of implementing the CLI enhancements and version management.

5.  **Version Management:**
    *   Investigate using a tool or script to automatically increment the version in [`pyproject.toml`](pyproject.toml) before publishing. Hatchling might have built-in support or require a script.
    *   Determine the best approach for version incrementing (e.g., patch, minor).
    *   Integrate the version incrementing step into the publishing workflow.

6.  **Subtask Creation:**
    *   Spawn a new task in 'code' mode to:
        *   Implement the command-line interface enhancements in `src/roo_conf/deploy.py`.
        *   Implement or configure the automatic version incrementing process.
        *   Update [`README.md`](README.md) with the new usage instructions.
        *   Append progress, challenges, and learnings for these new features to [`task.md`](task.md).
        *   Build and publish the package after implementing the features.

## Workflow Diagram

```mermaid
graph TD
    A[Start Task] --> B{Review Existing Files & Feedback};
    B --> C[Update Plan with New Requirements];
    C --> D[Update Documentation Files];
    D --> E[Spawn Code Subtask for Implementation & Publishing];
    E --> F[End Task];