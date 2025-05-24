# Implementation Task List for roo-conf

This file outlines the tasks for implementing new features and fixes in the `roo-conf` package.

## Tasks:

- Modify the `list_available_prompts` function in `src/roo_conf/deploy.py` to exclude the `.git` directory and its contents when iterating through files in the local templates directory (`~/.config/roo-conf/templates`).
- Ensure that only actual template files (e.g., markdown files) are listed from the remote source.
- Update documentation (if necessary) to reflect this fix.

## Implement `sync-modes` Command:

- Add a new subcommand `sync-modes` to the `roo-conf` CLI using `argparse`.
- Implement a function `find_vscode_settings_paths` to locate the `settings` directories for VS Code and VS Code Insiders on POSIX systems using conventional paths (`~/.vscode-server[-insiders]/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/`).
- In the `sync-modes` command logic, use `find_vscode_settings_paths` to get the paths to the `custom_modes.yaml` files.
- Verify the existence of the `custom_modes.yaml` files at the determined paths.
- Determine the latest version of `custom_modes.yaml` by comparing file modification timestamps.
- Read the content of the latest `custom_modes.yaml` file.
- Copy the content of the latest file to the other location(s) where `custom_modes.yaml` exists.
- Implement error handling for file not found or other issues during synchronization.
- Add basic reporting to indicate which file was synchronized and where it was copied.
- Structure the path-finding logic for future extension to Windows.
- Integrate the `sync-modes` subcommand into the main `roo-conf` entry point.

## Completed Tasks:

- Modified `list_available_prompts` to exclude the `.git` directory and list only markdown files from the remote templates directory.
- Implemented the `sync-modes` command to synchronize `custom_modes.yaml` files between VS Code and VS Code Insiders installations.
- Refactored the logic for finding and storing VS Code settings paths into a new module (`src/roo_conf/settings_manager.py`).
- Ensured synchronization occurs if at least one `custom_modes.yaml` file exists and potential settings directories are found.
- Copied the latest `custom_modes.yaml` to the remote templates directory (`~/.config/roo-conf/templates`).
- Updated `README.md` to document the changes.