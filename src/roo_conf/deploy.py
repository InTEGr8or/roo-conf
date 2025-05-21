import os
import pathlib
import importlib.resources
import argparse
import subprocess
import sys
import json
import shutil

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

def list_available_prompts(args):
    """
    Lists available prompt files from the package or remote source.
    """
    config = get_config()
    template_source_repo = config.get('template_source_repo')

    print("Available prompts:")
    found_prompts = False

    if template_source_repo and TEMPLATES_DIR.exists():
        # List from remote source
        for root, _, files in os.walk(TEMPLATES_DIR):
            for file in files:
                relative_path = pathlib.Path(root) / file
                # Make path relative to TEMPLATES_DIR for display
                display_path = relative_path.relative_to(TEMPLATES_DIR)
                print(f"- {display_path}")
                found_prompts = True
    else:
        # List from package resources
        package_prompts_dir = importlib.resources.files('roo_conf.prompts')
        for item in package_prompts_dir.iterdir():
            if item.is_file():
                print(f"- {item.name} (package)")
                found_prompts = True

    if not found_prompts:
        print("No prompt files found.")


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
    in the current working directory.
    """
    current_working_dir = pathlib.Path.cwd()
    target_dir = current_working_dir / ".roo"

    # Create the target directory if it doesn't exist
    target_dir.mkdir(exist_ok=True)

    config = get_config()
    template_source_repo = config.get('template_source_repo')
    source_dir = None

    if template_source_repo and TEMPLATES_DIR.exists():
        print("Using remote template source.")
        # Iterate through files in the source directory recursively
        for root, _, files in os.walk(TEMPLATES_DIR):
            for file in files:
                source_path = pathlib.Path(root) / file
                # Construct target path based on relative path from TEMPLATES_DIR
                relative_target_path = source_path.relative_to(TEMPLATES_DIR)
                target_file_path = target_dir / relative_target_path

                # Ensure target subdirectory exists
                target_file_path.parent.mkdir(parents=True, exist_ok=True)

                try:
                    content = source_path.read_text()

                    # Replace the placeholder (only if it's a text file, assuming .md for now)
                    # A more robust solution might involve checking file type or content
                    if source_path.suffix == '.md':
                         updated_content = content.replace('{{repo-full-path}}', str(current_working_dir))
                    else:
                         updated_content = content


                    # Write the updated content to the target file
                    with open(target_file_path, 'w') as f:
                        f.write(updated_content)

                    print(f"Deployed {source_path.relative_to(TEMPLATES_DIR)} to {target_file_path}")

                except Exception as e:
                    print(f"Error deploying {source_path.relative_to(TEMPLATES_DIR)}: {e}")

    else:
        print("Using package template source.")
        source_dir = importlib.resources.files('roo_conf.prompts')

        # Iterate through files in the package prompts directory
        for item in source_dir.iterdir():
            if item.is_file():
                source_filename = item.name
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


def edit_prompt(args):
    """
    Opens a deployed prompt file in the configured editor.
    """
    config = get_config()
    editor = config.get('editor')

    if not editor:
        print("No editor configured. Please set your preferred editor using 'roo-conf config editor <editor_command>'.")
        return

    file_name = args.file_name
    if not file_name:
        list_available_prompts(args) # Pass args here as well
        return

    # Construct the expected deployed path, including subdirectories if the file_name contains them
    deployed_path = get_deployed_path(file_name)

    if not deployed_path.exists():
        print(f"Error: Deployed file '{file_name}' not found at {deployed_path}")
        return

    try:
        subprocess.run([editor, str(deployed_path)])
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
    deploy_parser.set_defaults(func=deploy_prompts)

    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit a deployed prompt file.")
    edit_parser.add_argument(
        "file_name",
        nargs="?", # Makes the argument optional
        help="Name of the prompt file to edit (without .md extension)."
    )
    edit_parser.set_defaults(func=edit_prompt)

    # Config command
    config_parser = subparsers.add_parser("config", help="Configure roo-conf settings.")
    config_parser.add_argument(
        "key",
        help="Configuration key (e.g., 'editor', 'template_source_repo')."
    )
    config_parser.add_argument(
        "value",
        help="Configuration value."
    )
    config_parser.set_defaults(func=lambda args: set_config(args.key, args.value))

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