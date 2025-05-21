# Plan for Converting Bash Script to Python Package (roo-conf)

This document outlines the steps to convert a bash script that deploys configuration files into a Python package executable via `uvx roo-conf`, including new requirements for version management and command-line interface enhancements, automated publishing via GitHub Actions, and the ability to pull prompt templates from a remote Git repository using sparse checkout.

## Objective

Create a Python package `roo-conf` that can be installed and executed using `uvx`. The package will deploy markdown files from either its package resources or a configured remote Git repository (pulled using sparse checkout) to a `.roo` directory in the current working directory, removing the `.md` extension and replacing a `{{repo-full-path}}` placeholder with the current repository path. The package will provide command-line interfaces for deploying, editing, configuring, and pulling prompt templates. Automated publishing to PyPI will be handled by a GitHub Actions workflow triggered by version changes.

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
*   A local directory for cloned templates (e.g., `~/.config/roo-conf/templates`) will be used for sparse checkout.

## Detailed Plan

1.  **Project Structure:**
    *   The markdown files are located in `src/roo_conf/prompts/`.
    *   The bash script [`transfer-to-repo.sh`](docs/source/roo/transfer-to-repo.sh) is kept in `docs/source/roo/` for reference.
    *   Documentation files (`README.md`, `plan.md`, `task.md`) are in the project root.
    *   Version management script (`increment_version.py`) and a local build script (`publish.sh`) are in the project root.
    *   A GitHub Actions workflow file (`.github/workflows/workflow.yml`) exists for automated publishing.
    *   A local directory for cloned templates (e.g., `~/.config/roo-conf/templates`) will be used for sparse checkout.

2.  **Address uvx/Local Execution:**
    *   Confirm that the `[project.scripts]` section in [`pyproject.toml`](pyproject.toml) only contains the entry point for `roo-conf` pointing to a Python function (`roo_conf.deploy:deploy_prompts`).
    *   Understand that the persistent `uvx roo-conf` error is likely due to `uvx` caching a previously built and published wheel that contained an invalid console script entry.
    *   Recommend using `uv run roo-conf` for local execution of the package's console script, as this reliably uses the local environment and avoids the `uvx` caching issue.

3.  **Automated Publishing with GitHub Actions:**
    *   The `publish.sh` script has been modified to remove the version incrementing step and serves primarily as a local build script. (Completed)
    *   A GitHub Actions workflow in `.github/workflows/workflow.yml` is configured to trigger on pushes to tags (`v*`), build the package, and publish it to PyPI using a secure method for authentication. (Completed)

4.  **Implement Remote Template Source:**
    *   Modify `src/roo_conf/deploy.py` to add a new subcommand `pull` using `argparse`. (Completed)
    *   Implement the `pull` command logic to: (Completed)
        *   Read the `template_source_repo` URL from the configuration file (`~/.config/roo-conf/config.json`). (Completed)
        *   If the URL is configured, clone the repository to a designated local directory (e.g., `~/.config/roo-conf/templates`) using `git clone --depth 1 --sparse <repo_url> <local_path>`. (Completed)
        *   If the directory already exists, navigate into it and use `git pull` to update. (Completed)
        *   Configure sparse checkout to include only the necessary markdown files or directories within the cloned repository. (TODO: Sparse checkout configuration needs to be implemented after cloning)
        *   Include error handling for git commands and configuration issues. (Completed)
    *   Modify the `deploy_prompts` function in `src/roo_conf/deploy.py` to: (Completed)
        *   Check if `template_source_repo` is configured and the local templates directory exists. (Completed)
        *   If so, read markdown files from the local templates directory. (Completed)
        *   If not, fall back to reading markdown files from the package resources (`roo_conf.prompts`). (Completed)
    *   Add support for configuring `template_source_repo` using the `config` subcommand. (Completed)

5.  **Documentation Files:**
    *   Update [`README.md`](README.md) to include instructions for configuring `template_source_repo`, using the `pull` command (mentioning sparse checkout), and explaining how the `deploy` command uses the configured source. (Completed)
    *   Update [`task.md`](task.md) to create a new task list for the implementation of the remote template source feature, specifying the use of sparse checkout. (Completed)
    *   [`plan.md`](plan.md) has been updated to reflect the new feature and sparse checkout approach. (Completed)

6.  **Final Review:**
    *   Review the implemented code and documentation to ensure all requirements from `task.md` are met. (TODO)
    *   Implement the sparse checkout configuration after cloning in the `pull` command. (TODO)

## Workflow Diagram

```mermaid
graph TD
    A[Start Task] --> B{Review Feedback & Code};
    B --> C[Update Plan with New Feature & Sparse Checkout];
    C --> D[Update task.md with Sparse Checkout];
    D --> E[Implement Remote Template Source & Update Documentation];
    E --> F[Final Review and Sparse Checkout Configuration];
    F --> G[End Task];