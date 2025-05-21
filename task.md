# Implementation Task List for roo-conf (Remote Template Source Feature)

This file outlines the tasks to be completed for implementing the ability to pull prompt templates from a remote Git repository.

## Tasks:

- [x] Modify `src/roo_conf/deploy.py` to add a new subcommand `pull` using `argparse`.
- [x] Implement the `pull` command logic to:
    - [x] Read the `template_source_repo` URL from the configuration file (`~/.config/roo-conf/config.json`).
    - [x] If the URL is configured:
        - [x] If the local templates directory (e.g., `~/.config/roo-conf/templates`) does not exist, clone the repository using `git clone --depth 1 <repo_url> <local_path>`. (Changed from sparse checkout for simplicity and effectiveness)
        - [x] If the local templates directory exists, remove it and re-clone to ensure a clean state.
    - [x] Include error handling for git commands and configuration issues.
- [x] Modify the `deploy_prompts` function in `src/roo_conf/deploy.py` to:
    - [x] Check if `template_source_repo` is configured and the local templates directory exists.
    - [x] If so, read files recursively from the local templates directory.
    - [x] If not, fall back to reading files from the package resources (`roo_conf.prompts`).
- [x] Modify the `list_available_prompts` function to recursively list files from the remote source if configured.
- [x] Add support for configuring `template_source_repo` using the `config` subcommand in `src/roo_conf/deploy.py`.
- [x] Update `README.md` to include instructions for configuring `template_source_repo`, using the `pull` command, and explaining how the `deploy` command uses the configured source.
- [x] Update `plan.md` and `task.md` to reflect the implementation of this feature.