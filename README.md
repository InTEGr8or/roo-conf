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

Navigate to the root directory of your Git repository in the terminal. Then, execute the `roo-conf` command using `uvx`:

```bash
uvx roo-conf
```

This will create a `.roo` directory in your current repository (if it doesn't exist) and copy the necessary configuration files into it, replacing the `{{repo-full-path}}` placeholder with the absolute path to your repository.