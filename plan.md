# Plan for Converting Bash Script to Python Package (roo-conf)

This document outlines the steps to convert a bash script that deploys configuration files into a Python package executable via `uvx roo-conf`, including new requirements for version management and command-line interface enhancements, and automated publishing via GitHub Actions.

## Objective

Create a Python package `roo-conf` that can be installed and executed using `uvx`. The package will deploy markdown files stored within it to a `.roo` directory in the current working directory, removing the `.md` extension and replacing a `{{repo-full-path}}` placeholder with the current repository path. The package will provide a command-line interface for listing or indicating specific deployed files. Automated publishing to PyPI will be handled by a GitHub Actions workflow triggered by version changes.

## Current State

*   Initial Python package structure created using `uv init --package --lib`.
*   Existing files: `.gitignore`, `.python-version`, [`pyproject.toml`](pyproject.toml), [`README.md`](README.md), `src/`, [`src/roo_conf/__init__.py`](src/roo_conf/__init__.py), [`src/roo_conf/py.typed`](src/roo_conf/py.typed).
*   Markdown files (`system-prompt-architect-gh.md`, `system-prompt-code-gh.md`) are located in `src/roo_conf/prompts/`.
*   The original bash script (`transfer-to-repo.sh`) is located in `docs/source/roo/` for reference.
*   Documentation files (`README.md`, `plan.md`, `task.md`) are in the project root.
*   Initial Python deployment logic is in `src/roo_conf/deploy.py`.
*   `pyproject.toml` has the `[project.scripts]` entry point for `roo-conf`.
*   Automatic version incrementing script (`increment_version.py`) and a local publishing script (`publish.sh`) exist.

## Detailed Plan

1.  **Project Structure:**
    *   The markdown files are located in `src/roo_conf/prompts/`.
    *   The bash script [`transfer-to-repo.sh`](docs/source/roo/transfer-to-repo.sh) is kept in `docs/source/roo/` for reference.
    *   Documentation files (`README.md`, `plan.md`, `task.md`) are in the project root.
    *   Version management script (`increment_version.py`) and a local build script (`publish.sh`) are in the project root.
    *   A GitHub Actions workflow file (`.github/workflows/workflow.yml`) will be created for automated publishing.

2.  **Address uvx/Local Execution:**
    *   Confirm that the `[project.scripts]` section in [`pyproject.toml`](pyproject.toml) only contains the entry point for `roo-conf` pointing to a Python function (`roo_conf.deploy:deploy_prompts`).
    *   Understand that the persistent `uvx roo-conf` error is likely due to `uvx` caching a previously built and published wheel that contained an invalid console script entry.
    *   Recommend using `uv run roo-conf` for local execution of the package's console script, as this reliably uses the local environment and avoids the `uvx` caching issue.

3.  **Automated Publishing with GitHub Actions:**
    *   Modify the `publish.sh` script to remove the version incrementing step. It will now serve primarily as a local build script. (Completed)
    *   Create a new file `.github/workflows/workflow.yml` with a GitHub Actions workflow. (Completed)
    *   Configure the workflow to trigger on pushes to tags (e.g., `v*`).
    *   Define steps in the workflow to:
        *   Checkout the code.
        *   Set up Python.
        *   Install `uv`.
        *   Build the source distribution and wheel using `uv build`.
        *   Publish the built package to PyPI using `uv publish`, utilizing a secure method for authentication (e.g., PyPI trusted publisher or a PyPI API token stored as a GitHub Secret).

4.  **Documentation Files:**
    *   Update [`README.md`](README.md) to explain the recommended local execution method (`uv run`) and the automated publishing process via GitHub Actions. (Completed)
    *   Update [`task.md`](task.md) to reflect the completed investigation steps and the implementation of the GitHub Actions workflow. (Completed)
    *   [`plan.md`](plan.md) has been updated to reflect the new publishing strategy. (Completed)

## Workflow Diagram

```mermaid
graph TD
    A[Start Task] --> B{Review Feedback & Error};
    B --> C[Update Plan for CI/CD Publishing];
    C --> D[Modify publish.sh];
    D --> E[Create GitHub Workflow];
    E --> F[Update Documentation];
    F --> G[End Task];