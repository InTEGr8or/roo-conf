# Plan for Converting Bash Script to Python Package (roo-conf)

This document outlines the steps to convert a bash script that deploys configuration files into a Python package executable via `uvx roo-conf`.

## Objective

Create a Python package `roo-conf` that can be installed and executed using `uvx`. The package will deploy markdown files stored within it to a `.roo` directory in the current working directory, removing the `.md` extension and replacing a `{{repo-full-path}}` placeholder with the current repository path.

## Current State

*   Initial Python package structure created using `uv init --package --lib`.
*   Existing files: `.gitignore`, `.python-version`, [`pyproject.toml`](pyproject.toml), [`README.md`](README.md), `src/`, [`src/roo_conf/__init__.py`](src/roo_conf/__init__.py), [`src/roo_conf/py.typed`](src/roo_conf/py.typed).
*   Markdown files (`system-prompt-architect-gh`, `system-prompt-code-gh`) and the original bash script (`transfer-to-repo.sh`) are located in `docs/source/roo/`.

## Detailed Plan

1.  **Project Structure:**
    *   The markdown files will be moved from `docs/source/roo/` to a new directory within the Python package: `src/roo_conf/prompts/`.
    *   The bash script [`transfer-to-repo.sh`](docs/source/roo/transfer-to-repo.sh) will be kept in `docs/source/roo/` for reference but will not be part of the Python package.
    *   New documentation files (`README.md`, `plan.md`, `task.md`) will be created in the project root (`/home/mstouffer/repos/roo-conf`).

2.  **Python Implementation (`src/roo_conf/deploy.py`):**
    *   Create a new file `src/roo_conf/deploy.py`.
    *   Import necessary modules: `os`, `pathlib`, `importlib.resources`.
    *   Define a main function, e.g., `deploy_prompts()`.
    *   Inside `deploy_prompts()`:
        *   Get the current working directory using `pathlib.Path.cwd()`.
        *   Define the target directory path: `current_working_dir / ".roo"`.
        *   Create the target directory if it doesn't exist: `target_dir.mkdir(exist_ok=True)`.
        *   Use `importlib.resources.files('roo_conf.prompts')` to access the directory containing the markdown files within the installed package.
        *   Iterate through the files in the package resource directory.
        *   For each file ending with `.md`:
            *   Read the content using `importlib.resources.read_text('roo_conf.prompts', filename)`.
            *   Replace `{{repo-full-path}}` with the `current_working_dir` path string.
            *   Determine the output filename by removing the `.md` extension: `filename.replace('.md', '')`.
            *   Write the modified content to `target_dir / output_filename`.
    *   Add a standard `if __name__ == "__main__":` block to call `deploy_prompts()`.

3.  **`pyproject.toml` Update:**
    *   Add a `[project.scripts]` section to [`pyproject.toml`](pyproject.toml).
    *   Define the entry point for the `roo-conf` command:
        ```toml
        [project.scripts]
        roo-conf = "roo_conf.deploy:deploy_prompts"
        ```
    *   Add `importlib_resources` as a dependency if targeting Python versions older than 3.9 (though `uv` might handle this). Given `requires-python = ">=3.12"`, `importlib.resources` is built-in.

4.  **Documentation Files:**
    *   Write content for [`README.md`](README.md) explaining the package's purpose, installation (using `uv`), and usage (`uvx roo-conf`). (Completed)
    *   Write the current plan into a new file [`plan.md`](plan.md). (Current Step)
    *   Create an empty [`task.md`](task.md) file to be updated by the implementation subtask.

5.  **File Migration:**
    *   Create the directory `src/roo_conf/prompts/`.
    *   Move `docs/source/roo/system-prompt-architect-gh` to `src/roo_conf/prompts/system-prompt-architect-gh.md`.
    *   Move `docs/source/roo/system-prompt-code-gh` to `src/roo_conf/prompts/system-prompt-code-gh.md`.
    *   Move any other relevant markdown files from `docs/source/roo/` to `src/roo_conf/prompts/` and add the `.md` extension.

6.  **Subtask Creation:**
    *   Once the plan is approved and the documentation files are created, I will spawn a new task in 'code' mode.
    *   This subtask will be responsible for implementing the Python code in `src/roo_conf/deploy.py`, updating [`pyproject.toml`](pyproject.toml), and appending its progress and any challenges/learnings to [`task.md`](task.md).

## Workflow Diagram

```mermaid
graph TD
    A[Start Task] --> B{Review Existing Files};
    B --> C[Define Package Structure];
    C --> D[Outline Python Logic];
    D --> E[Update pyproject.toml];
    E --> F[Create/Update Docs];
    F --> G[Move & Rename Files];
    G --> H[Present Plan];
    H --> I{User Approval};
    I -- Yes --> J[Execute Plan Steps];
    J --> K[Spawn Code Subtask];
    K --> L[End Task];
    I -- No --> H;