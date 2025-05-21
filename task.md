# Implementation Task List for roo-conf (Componentized Deploy & Edit Refactor)

This file outlines the tasks to be completed for implementing componentized template deployment and refactoring the edit command.

## Tasks:

- [x] Modify the `deploy` subcommand in `src/roo_conf/deploy.py` to accept optional arguments for template components (e.g., `cdk`, `typescript`).
- [x] Define a mechanism to map component names to specific files or directories within the template source (package resources or remote clone). This might involve a configuration file or convention. (Implemented using glob patterns for remote source and exact file names for package resources).
- [x] Modify the `deploy_prompts` function in `src/roo_conf/deploy.py` to:
    - [x] Always include default system prompts.
    - [x] Include templates corresponding to the specified components.
    - [x] Handle glob patterns (e.g., `cdk/**/*.*`) for component selection (for remote source).
    - [x] Read the selected files from the appropriate source (package or local clone).
    - [x] Deploy the selected files to the `.roo` directory.
- [x] Modify the `edit` subcommand in `src/roo_conf/deploy.py` to open the *source* template file instead of the deployed file.
- [x] Determine the source file path for the `edit` command based on whether a remote template source is configured and the file exists there, or if it's a package resource. (Editing of package resources is not supported directly).
- [x] Update the logic in the `edit` command to open the correct source file using the configured editor.
- [x] Update the `list_available_prompts` function (used by `edit` without arguments) to clearly indicate whether templates are from package resources or the remote source.
- [x] Update `README.md` to include instructions for componentized deployment and the refactored `edit` command.
- [x] Update `plan.md` and `task.md` to reflect the implementation of these features (this will be done after the implementation is complete).