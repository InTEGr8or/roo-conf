# Plan for Converting Bash Script to Python Package (roo-conf)

This document outlines the steps to convert a bash script that deploys configuration files into a Python package executable via `uvx roo-conf`, including new requirements for version management and command-line interface enhancements, automated publishing via GitHub Actions, the ability to pull prompt templates from a remote Git repository, componentized template deployment, and editing source template files.

## Objective

Create a Python package `roo-conf` that can be installed and executed using `uvx`. The package will deploy selected markdown files from either its package resources or a configured remote Git repository (pulled using a depth-1 clone) to a `.roo` directory in the current working directory, removing the `.md` extension and replacing a `{{repo-full-path}}` placeholder with the current repository path. The package will provide command-line interfaces for deploying (with component selection), editing source templates, configuring, and pulling prompt templates. Automated publishing to PyPI will be handled by a GitHub Actions workflow triggered by version changes.

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

1.  **Project Structure:**
    *   The markdown files are located in `src/roo_conf/prompts/`.
    *   The bash script [`transfer-to-repo.sh`](docs/source/roo/transfer-to-repo.sh) is kept in `docs/source/roo/` for reference.
    *   Documentation files (`README.md`, `plan.md`, `task.md`) are in the project root.
    *   Version management script (`increment_version.py`) and a local build script (`publish.sh`) are in the project root.
    *   A GitHub Actions workflow file (`.github/workflows/workflow.yml`) exists for automated publishing.
    *   A local directory for cloned templates (e.g., `~/.config/roo-conf/templates`) is used for storing remote templates.

2.  **Address uvx/Local Execution:**
    *   Confirm that the `[project.scripts]` section in [`pyproject.toml`](pyproject.toml) only contains the entry point for `roo-conf` pointing to a Python function (`roo_conf.deploy:deploy_prompts`).
    *   Understand that the persistent `uvx roo-conf` error is likely due to `uvx` caching a previously built and published wheel that contained an invalid console script entry.
    *   Recommend using `uv run roo-conf` for local execution of the package's console script, as this reliably uses the local environment and avoids the `uvx` caching issue.

3.  **Automated Publishing with GitHub Actions:**
    *   The `publish.sh` script has been modified to remove the version incrementing step and serves primarily as a local build script. (Completed)
    *   A GitHub Actions workflow in `.github/workflows/workflow.yml` is configured to trigger on pushes to tags (`v*`), build the package, and publish it to PyPI using a secure method for authentication. (Completed)

4.  **Implement Remote Template Source:**
    *   The `pull` subcommand has been added to `src/roo_conf/deploy.py`. (Completed)
    *   The `pull` command logic has been implemented to clone the `template_source_repo` using `git clone --depth 1` and re-clone for updates. Error handling is included. (Completed)
    *   The `deploy_prompts` function has been modified to read markdown files from the local templates directory if configured, falling back to package resources otherwise. (Completed)
    *   Support for configuring `template_source_repo` using the `config` subcommand has been added. (Completed)
    *   The `list_available_prompts` function has been modified to list from the remote source if configured. (Completed)

5.  **Componentized Template Deployment:**
    *   Modify the `deploy` subcommand in `src/roo_conf/deploy.py` to accept optional arguments for template components (e.g., `cdk`, `typescript`). (Completed)
    *   Define a mechanism to map component names to specific files or directories within the template source (package resources or remote clone). This might involve a configuration file or convention. (Completed)
    *   Modify the `deploy_prompts` function to:
        *   Always include default system prompts. (Completed)
        *   Include templates corresponding to the specified components. (Completed)
        *   Handle glob patterns (e.g., `cdk/**/*.*`) for component selection. (Completed)
        *   Read the selected files from the appropriate source (package or local clone). (Completed)
        *   Deploy the selected files to the `.roo` directory. (Completed)

6.  **Refactor Edit Command:**
    *   Modify the `edit` subcommand in `src/roo_conf/deploy.py` to open the *source* template file instead of the deployed file. (Completed)
    *   Determine the source file path based on whether a remote template source is configured and the file exists there, or if it's a package resource. (Completed)
    *   Update the logic to open the correct source file using the configured editor. (Completed)
    *   Update the `list_available_prompts` function (used by `edit` without arguments) to clearly indicate whether templates are from package resources or the remote source. (Completed)

7.  **Documentation Files:**
    *   Update [`README.md`](README.md) to include instructions for componentized deployment and the refactored `edit` command. (Completed)
    *   Update [`task.md`](task.md) to reflect the implementation of these features. (Completed)
    *   [`plan.md`](plan.md) has been updated to reflect the implementation of these features. (Completed)

8.  **Spawn Code-GH Subtask:**
    *   Spawn a new task in 'Code-GH' mode to implement the changes outlined in steps 5 and 6 and update the documentation files as described in step 7. (Completed)

## Workflow Diagram

```mermaid
graph TD
    A[Start Task] --> B{Review Feedback & Code};
    B --> C[Update Plan with Componentized Deploy & Edit Refactor];
    C --> D[Update task.md for New Features];
    D --> E[Spawn Code-GH Subtask for Implementation];
    E --> F[End Task];