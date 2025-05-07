# roo-conf

A Python package to deploy configuration and prompt files for Roo Code into a repository.

## Purpose

This package provides a command-line utility (`roo-conf`) that copies specific configuration and prompt files from the installed package to a `.roo` directory within the current working directory of a Git repository. This allows for easy deployment and management of Roo Code configurations across different projects.

## Installation

You can install `roo-conf` using `uv`:

```bash
uv pip install roo-conf
```

## Usage

Navigate to the root directory of your Git repository in the terminal. Then, execute the `roo-conf` command using `uvx`.

By default, running `uvx roo-conf` will create a `.roo` directory in your current repository (if it doesn't exist) and copy the necessary configuration files into it, replacing the `{{repo-full-path}}` placeholder with the absolute path to your repository.

You can also use the `roo-conf` command with the following options:

*   **List available prompts:** To see a list of all available prompt files in the package (without the `.md` extension), run:

    ```bash
    uvx roo-conf --list
    ```

*   **Locate a deployed prompt:** To find the expected path of a specific deployed prompt file (without the `.md` extension) in your `.roo` directory, use the `--file` or `-f` argument:

    ```bash
    uvx roo-conf --file <prompt_name>
    # or
    uvx roo-conf -f <prompt_name>
    ```

    Replace `<prompt_name>` with the name of the prompt file you want to locate (e.g., `system-prompt-code-gh`). The command will output the full path to the file within the `.roo` directory.