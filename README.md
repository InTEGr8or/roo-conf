# roo-conf

A Python package to deploy configuration and prompt files for Roo Code into a repository.

## Purpose

This package provides a command-line utility (`roo-conf`) that copies specific configuration and prompt files from either the installed package or a configured remote Git repository to a `.roo` directory within the current working directory of a Git repository. This allows for easy deployment and management of Roo Code configurations across different projects.

## Installation

You can install `roo-conf` using `uv`:

```bash
uv pip install roo-conf
```

## Usage

The `roo-conf` command supports several subcommands: `deploy`, `edit`, `config`, and `pull`.

**Note:** While `uvx roo-conf` is the intended way to run installed console scripts, there seems to be a caching issue with `uvx` that prevents it from picking up the latest changes to the package metadata, resulting in an "invalid console script" error. Until this is resolved, it is recommended to use `uv run roo-conf` to execute the package's commands within the project's virtual environment.

### Deploying Prompts (Componentized)

Navigate to the root directory of your Git repository in the terminal. Then, execute the `deploy` subcommand using `uv run`.

You can now deploy specific components of the template by providing their names or glob patterns as arguments. Default system prompts are always included.

```bash
uv run roo-conf deploy [component1] [component2] ...
```

Replace `[component1] [component2] ...` with the names of the components or glob patterns you want to deploy (e.g., `cdk`, `typescript/**/*`).

If no components are specified, all available templates from the configured source will be deployed.

This will create a `.roo` directory in your current repository (if it doesn't exist) and copy the necessary configuration files into it, replacing the `{{repo-full-path}}` placeholder with the absolute path to your repository. If a remote template source is configured and available, it will use templates from there; otherwise, it will fall back to using templates included in the package.

### Editing Source Template Files

To edit a source template file, use the `edit` subcommand followed by the template file name. The file will be opened using your configured editor.

```bash
uv run roo-conf edit <template_name>
```

Replace `<template_name>` with the name of the template file you want to edit (e.g., `system-prompt-code-gh.md`). Note that you should now provide the full file name, including the extension.

The `edit` command will attempt to open the source file from your configured remote template repository first. If a remote source is not configured or the file is not found there, it will indicate that the file is a package resource and cannot be edited directly.

If you run the `edit` subcommand without a filename, it will list the available template files from the configured source (remote if configured and available, otherwise package), indicating the source for each.

```bash
uv run roo-conf edit
```

### Configuring roo-conf

To set configuration options for `roo-conf`, use the `config` subcommand followed by the key and value. You can configure your preferred editor and the remote template source repository.

```bash
uv run roo-conf config editor <editor_command>
```

Replace `<editor_command>` with the command to launch your preferred text editor (e.g., `code`, `nano`, `vim`).

```bash
uv run roo-conf config template_source_repo <repo_url>
```

Replace `<repo_url>` with the URL of the Git repository containing your prompt templates. This setting is stored in a configuration file in your user's home directory (`~/.config/roo-conf/config.json`).

### Pulling Remote Templates

If you have configured a remote template source repository, you can pull the latest templates using the `pull` subcommand. This will clone the repository (if it doesn't exist locally) or pull updates using sparse checkout to only fetch markdown files.

```bash
uv run roo-conf pull
```

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