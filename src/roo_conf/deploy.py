import os
import pathlib
import importlib.resources
import argparse
import subprocess
import sys
import json
import shutil
import glob

CONFIG_DIR = pathlib.Path("~/.config/roo-conf").expanduser()
CONFIG_FILE = CONFIG_DIR / "config.json"
TEMPLATES_DIR = CONFIG_DIR / "templates"

def get_config():
    """Reads the configuration file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def set_config(key, value):
    """Writes a key-value pair to the configuration file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config = get_config()
    config[key] = value
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuration updated: {key} = {value}")

def print_config():
    """Prints the current configuration."""
    config = get_config()
    if config:
        print("Current configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    else:
        print("No configuration found.")


def list_available_prompts(args):
    """
    Lists available prompt files from the package or remote source,
    indicating the source.
    """
    config = get_config()
    template_source_repo = config.get('template_source_repo')

    print("Available prompts:")
    found_prompts = False

    if template_source_repo and TEMPLATES_DIR.exists():
        # List from remote source
        print("From remote source:")
        for root, dirs, files in os.walk(TEMPLATES_DIR):
            # Exclude .git directory
            if '.git' in dirs:
                dirs.remove('.git')

            for file in files:
                relative_path = pathlib.Path(root) / file
                # Make path relative to TEMPLATES_DIR for display
                display_path = relative_path.relative_to(TEMPLATES_DIR)
                print(f"- {display_path}")
                found_prompts = True

    # List from package resources
    # Always list package resources, even if remote is configured, for completeness
    print("From package resources:")
    package_prompts_dir = importlib.resources.files('roo_conf.prompts')
    package_files = [item.name for item in package_prompts_dir.iterdir() if item.is_file()]
    if package_files:
        for file_name in package_files:
            print(f"- {file_name}")
        found_prompts = True
    else:
        print("No package resources found.")


    if not found_prompts:
        print("No prompt files found from either source.")


def get_deployed_path(file_name):
    """
    Gets the expected path of a deployed prompt file.
    """
    current_working_dir = pathlib.Path.cwd()
    target_dir = current_working_dir / ".roo"
    target_file_path = target_dir / file_name
    return target_file_path

def deploy_prompts(args):
    """
    Deploys prompt files from the configured source to the .roo directory
    in the current working directory, optionally filtering by components.
    """
    current_working_dir = pathlib.Path.cwd()
    target_dir = current_working_dir / ".roo"

    # Create the target directory if it doesn't exist
    target_dir.mkdir(exist_ok=True)

    config = get_config()
    template_source_repo = config.get('template_source_repo')

    # Always include default system prompts
    default_prompts = ["system-prompt-architect-gh.md", "system-prompt-code-gh.md"]
    components = args.components if args.components else []

    print(f"Deploying components: {components if components else 'all'}")

    if template_source_repo and TEMPLATES_DIR.exists():
        print("Using remote template source.")
        source_base_dir = TEMPLATES_DIR
        all_source_files = [pathlib.Path(root) / file for root, _, files in os.walk(source_base_dir) for file in files]

        files_to_deploy = []
        if components:
            for component in components:
                # Treat component as a glob pattern relative to the source_base_dir
                pattern = str(source_base_dir / component)
                files_to_deploy.extend(glob.glob(pattern, recursive=True))
        else:
            # If no components specified, deploy all files from the remote source
            files_to_deploy = [str(f) for f in all_source_files]

        # Add default prompts if they are not already included and exist in the source
        for default_prompt in default_prompts:
            default_path = source_base_dir / default_prompt
            if default_path.exists() and str(default_path) not in files_to_deploy:
                 files_to_deploy.append(str(default_path))


        for source_file_path_str in files_to_deploy:
            source_path = pathlib.Path(source_file_path_str)
            if not source_path.is_file():
                continue # Skip directories or non-files from glob results

            relative_target_path = source_path.relative_to(source_base_dir)
            target_file_path = target_dir / relative_target_path

            # Ensure target subdirectory exists
            target_file_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                content = source_path.read_text()

                # Replace the placeholder (only if it's a text file, assuming .md for now)
                if source_path.suffix == '.md':
                     updated_content = content.replace('{{repo-full-path}}', str(current_working_dir))
                else:
                     updated_content = content

                # Write the updated content to the target file
                with open(target_file_path, 'w') as f:
                    f.write(updated_content)

                print(f"Deployed {relative_target_path} to {target_file_path}")

            except Exception as e:
                print(f"Error deploying {relative_target_path}: {e}")

    else:
        print("Using package template source.")
        source_dir = importlib.resources.files('roo_conf.prompts')
        all_package_files = [item for item in source_dir.iterdir() if item.is_file()]

        files_to_deploy = []
        if components:
             # For package resources, components must match file names exactly for now
             # Glob patterns are not supported for package resources with this approach
             available_package_files = [item.name for item in all_package_files]
             for component in components:
                 if component in available_package_files:
                     files_to_deploy.append(component)
                 else:
                     print(f"Warning: Component '{component}' not found in package resources.")
        else:
            # If no components specified, deploy all files from the package
            files_to_deploy = [item.name for item in all_package_files]

        # Always include default prompts if they are not already included
        for default_prompt in default_prompts:
            if default_prompt not in files_to_deploy:
                 # Check if the default prompt exists in the package resources
                 try:
                     importlib.resources.read_text('roo_conf.prompts', default_prompt)
                     files_to_deploy.append(default_prompt)
                 except FileNotFoundError:
                     print(f"Warning: Default prompt '{default_prompt}' not found in package resources.")


        for source_filename in files_to_deploy:
            target_filename = source_filename
            target_file_path = target_dir / target_filename

            try:
                content = importlib.resources.read_text('roo_conf.prompts', source_filename)

                # Replace the placeholder (only if it's a text file, assuming .md for now)
                if pathlib.Path(source_filename).suffix == '.md':
                    updated_content = content.replace('{{repo-full-path}}', str(current_working_dir))
                else:
                    updated_content = content

                # Write the updated content to the target file
                with open(target_file_path, 'w') as f:
                    f.write(updated_content)

                print(f"Deployed {source_filename} to {target_file_path}")

            except Exception as e:
                print(f"Error deploying {source_filename}: {e}")


def get_source_path(file_name):
    """
    Determines the source path of a template file based on configuration.
    Returns the path if found in the remote source, otherwise returns None.
    Direct editing of package resources is not supported.
    """
    config = get_config()
    template_source_repo = config.get('template_source_repo')

    if template_source_repo and TEMPLATES_DIR.exists():
        # Check remote source first
        source_path = TEMPLATES_DIR / file_name
        if source_path.exists():
            return source_path

    return None # Not found in remote source or remote source not configured/available


def edit_prompt(args):
    """
    Opens a source template file in the configured editor.
    """
    config = get_config()
    editor = config.get('editor')

    if not editor:
        print("No editor configured. Please set your preferred editor using 'roo-conf config editor <editor_command>'.")
        return

    file_name = args.file_name
    if not file_name:
        list_available_prompts(args)
        return

    # Determine the source path
    source_path = get_source_path(file_name)

    if source_path is None:
        print(f"Error: Source file '{file_name}' not found in remote template source or cannot be edited directly from package resources.")
        return

    try:
        subprocess.run([editor, str(source_path)])
    except FileNotFoundError:
        print(f"Error: Editor command '{editor}' not found. Please ensure it's in your PATH or set the correct command using 'roo-conf config editor <editor_command>'.")
    except Exception as e:
        print(f"Error opening file with editor: {e}")


def pull_templates(args):
    """
    Pulls prompt templates from the configured remote Git repository.
    """
    config = get_config()
    template_source_repo = config.get('template_source_repo')

    if not template_source_repo:
        print("No remote template source repository configured. Use 'roo-conf config template_source_repo <repo_url>' to set it.")
        return

    if TEMPLATES_DIR.exists():
        print(f"Templates directory {TEMPLATES_DIR} already exists. Removing and re-cloning.")
        try:
            shutil.rmtree(TEMPLATES_DIR)
            print("Existing templates directory removed.")
        except OSError as e:
            print(f"Error removing existing templates directory: {e}")
            return

    print(f"Cloning repository {template_source_repo} into {TEMPLATES_DIR}")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", template_source_repo, str(TEMPLATES_DIR)],
            check=True
        )
        print("Repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
    except FileNotFoundError:
         print("Error: git command not found. Please ensure Git is installed and in your PATH.")


def main():
    parser = argparse.ArgumentParser(description="Manage roo-conf prompts.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy prompt files to the .roo directory.")
    deploy_parser.add_argument(
        "components",
        nargs="*", # 0 or more arguments
        help="Optional list of components (e.g., cdk, typescript) or glob patterns to deploy."
    )
    deploy_parser.set_defaults(func=deploy_prompts)

    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit a source template file.")
    edit_parser.add_argument(
        "file_name",
        nargs="?", # Makes the argument optional
        help="Name of the template file to edit."
    )
    edit_parser.set_defaults(func=edit_prompt)

    # Config command
    config_parser = subparsers.add_parser("config", help="Configure roo-conf settings.")
    config_parser.add_argument(
        "key",
        nargs="?", # Make key optional
        help="Configuration key (e.g., 'editor', 'template_source_repo')."
    )
    config_parser.add_argument(
        "value",
        nargs="?", # Make value optional
        help="Configuration value."
    )
    config_parser.set_defaults(func=lambda args: set_config(args.key, args.value) if args.key and args.value is not None else print_config())

    # Pull command
    pull_parser = subparsers.add_parser("pull", help="Pull prompt templates from the configured remote repository.")
    pull_parser.set_defaults(func=pull_templates)


    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()