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

The `roo-conf` command supports several subcommands: `deploy`, `edit`, and `config`.

**Note:** While `uvx roo-conf` is the intended way to run installed console scripts, there seems to be a caching issue with `uvx` that prevents it from picking up the latest changes to the package metadata, resulting in an "invalid console script" error. Until this is resolved, it is recommended to use `uv run roo-conf` to execute the package's commands within the project's virtual environment.

### Deploying Prompts

Navigate to the root directory of your Git repository in the terminal. Then, execute the `deploy` subcommand using `uv run`:

```bash
uv run roo-conf deploy
```

This will create a `.roo` directory in your current repository (if it doesn't exist) and copy the necessary configuration files into it, replacing the `{{repo-full-path}}` placeholder with the absolute path to your repository.

### Editing Deployed Prompts

To edit a deployed prompt file in your `.roo` directory, use the `edit` subcommand followed by the prompt file name (without the `.md` extension). The file will be opened using your configured editor.

```bash
uv run roo-conf edit <prompt_name>
```

Replace `<prompt_name>` with the name of the prompt file you want to edit (e.g., `system-prompt-code-gh`).

If you run the `edit` subcommand without a filename, it will list the available prompt files:

```bash
uv run roo-conf edit
```

### Configuring roo-conf

To set configuration options for `roo-conf`, use the `config` subcommand followed by the key and value. Currently, the only supported configuration is setting your preferred editor.

```bash
uv run roo-conf config editor <editor_command>
```

Replace `<editor_command>` with the command to launch your preferred text editor (e.g., `code`, `nano`, `vim`). This setting is stored in a configuration file in your user's home directory (`~/.config/roo-conf/config.json`).

## Development

### Building Locally

To build the package locally (create the source distribution and wheel), you can use the `./publish.sh` script. This script will:
1. Clear the `uv` cache.
2. Build the source distribution and wheel using `hatch build`.

```bash
./publish.sh
```

### Automated Publishing

Publishing to PyPI is automated via a GitHub Actions workflow. When a new Git tag starting with `v` (e.g., `v1.0.0`) is pushed to the repository, the workflow defined in `.github/workflows/workflow.yml` will trigger. This workflow will build the package and publish it to PyPI.

To publish a new version:
1. Manually update the `version` in `pyproject.toml`.
2. Commit the changes.
3. Create a new Git tag matching the version (e.g., `git tag v1.0.0`).
4. Push the commit and the tag (`git push && git push --tags`).

The GitHub Actions workflow requires a PyPI API token stored as a GitHub Secret named `PYPI_API_TOKEN` to authenticate with PyPI.