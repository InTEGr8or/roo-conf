# Implementation Task List for roo-conf

This file outlines the tasks for implementing new features and fixes in the `roo-conf` package.

## Implement `extract-conversations` Command:

- [x] Add a new subcommand `extract-conversations` to the `roo-conf` CLI using `argparse`. This subcommand should accept an optional argument for the target repository path, defaulting to the current working directory.
- [x] Implement logic to locate the global storage directories for both VS Code and VS Code Insiders (`~/.vscode-server[-insiders]/data/User/globalStorage/rooveterinaryinc.roo-cline/`).
- [ ] Determine the exact filename of the global state file within these directories that stores the "taskHistory".
    - **Information Gathered:** Searched known VS Code global storage paths for JSON files containing "taskHistory" but did not find a central file in a readable format. The `task.md` mentions `globalState.vscdb`, which is likely a SQLite database and cannot be read with current tools.
- [x] Construct the full paths to the global state files for both installations. (Based on the assumption of a readable file, which was not found).
- [ ] Read the content of the global state file(s). (Blocked by not finding a readable file).
- [ ] Parse the file content (assuming it's JSON) to extract the data associated with the "taskHistory" key. (Blocked by not finding a readable file).
- [x] Implement error handling for file not found or parsing errors when reading global state files. (Implemented based on the assumption of a readable file).
- [x] Iterate through the array of `HistoryItem` objects obtained from the task history. (This part of the code is written, but cannot be executed without loading the history).
- [x] For each `HistoryItem`, check if the `workspace` field exists and if its value matches the target repository path. (This part of the code is written, but cannot be executed without loading the history).
- [x] For each matching `HistoryItem`, construct the paths to the corresponding `api_conversation_history.json` and `ui_messages.json` files within the task's directory in `globalStorage`.
- [x] Read the content of `api_conversation_history.json` and `ui_messages.json`.
- [x] Implement error handling for file not found or parsing errors when reading conversation files.
- [x] Implement a function to convert the data from `api_conversation_history.json` and `ui_messages.json` into a single Markdown string, formatting conversation turns, roles, content, and timestamps.
- [x] Create a dedicated subfolder within the target repository to store the extracted conversations (e.g., `.roo-conf/conversations/`).
- [x] For each converted Markdown conversation, generate a unique and descriptive filename.
- [x] Write the Markdown content to a file with the generated filename within the `.roo-conf/conversations/` subfolder.
- [x] Implement error handling for writing Markdown files.
- [x] Report the number of conversations found and extracted.
- [x] Report any errors encountered during the extraction process.
- [x] Update [`README.md`](README.md) to describe the new `extract-conversations` command.

**Summary of Progress and Unfinished Parts:**

The command-line interface for `extract-conversations` is implemented, and the logic for locating storage directories, constructing conversation file paths, reading and converting conversation data to Markdown, and saving the output is in place with error handling. The `README.md` has been updated.

The main unfinished part is the inability to read and parse the central "taskHistory" data, which is required to identify which conversation directories belong to which workspace. This is blocked because the "taskHistory" appears to be stored in a SQLite database (`globalState.vscdb`) which cannot be accessed with the current tools, rather than a simple JSON file as initially assumed based on the task description's implication of JSON parsing.

Further work is needed to determine how to access the "taskHistory" from the VS Code global state, potentially requiring a different approach or tools to interact with the `.vscdb` file.