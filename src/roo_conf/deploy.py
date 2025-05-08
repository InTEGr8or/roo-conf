import os
import pathlib
import importlib.resources
import argparse
import subprocess
import sys
import json

CONFIG_DIR = pathlib.Path("~/.config/roo-conf").expanduser()
CONFIG_FILE = CONFIG_DIR / "config.json"

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

def list_available_prompts():
    """
    Lists available markdown prompt files from the package.
    """
    package_prompts_dir = importlib.resources.files('roo_conf.prompts')
    print("Available prompts:")
    found_prompts = False
    for item in package_prompts_dir.iterdir():
        if item.is_file() and item.name.endswith('.md'):
            print(f"- {item.name.replace('.md', '')}")
            found_prompts = True
    if not found_prompts:
        print("No markdown prompt files found in the package.")


def get_deployed_path(file_name):
    """
    Gets the expected path of a deployed prompt file.
    """
    current_working_dir = pathlib.Path.cwd()
    target_dir = current_working_dir / ".roo"
    target_file_path = target_dir / file_name
    return target_file_path

def deploy_prompts():
    """
    Deploys markdown prompt files from the package to the .roo directory
    in the current working directory.
    """
    current_working_dir = pathlib.Path.cwd()
    target_dir = current_working_dir / ".roo"

    # Create the target directory if it doesn't exist
    target_dir.mkdir(exist_ok=True)

    # Access the prompts directory within the installed package
    package_prompts_dir = importlib.resources.files('roo_conf.prompts')

    # Iterate through files in the package prompts directory
    for item in package_prompts_dir.iterdir():
        if item.is_file() and item.name.endswith('.md'):
            source_filename = item.name
            target_filename = source_filename.replace('.md', '')
            target_file_path = target_dir / target_filename

            try:
                # Read content from the package resource
                content = importlib.resources.read_text('roo_conf.prompts', source_filename)

                # Replace the placeholder
                updated_content = content.replace('{{repo-full-path}}', str(current_working_dir))

                # Write the updated content to the target file
                with open(target_file_path, 'w') as f:
                    f.write(updated_content)

                print(f"Deployed {source_filename} to {target_file_path}")

            except Exception as e:
                print(f"Error deploying {source_filename}: {e}")

def edit_prompt(file_name):
    """
    Opens a deployed prompt file in the configured editor.
    """
    config = get_config()
    editor = config.get('editor')

    if not editor:
        print("No editor configured. Please set your preferred editor using 'roo-conf config editor <editor_command>'.")
        return

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
    edit_parser.set_defaults(func=lambda args: edit_prompt(args.file_name) if args.file_name else list_available_prompts())

    # Config command
    config_parser = subparsers.add_parser("config", help="Configure roo-conf settings.")
    config_parser.add_argument(
        "key",
        help="Configuration key (e.g., 'editor')."
    )
    config_parser.add_argument(
        "value",
        help="Configuration value."
    )
    config_parser.set_defaults(func=lambda args: set_config(args.key, args.value))


    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()