import os
import pathlib
import importlib.resources
import argparse

def list_available_prompts():
    """
    Lists available markdown prompt files from the package.
    """
    package_prompts_dir = importlib.resources.files('roo_conf.prompts')
    print("Available prompts:")
    for item in package_prompts_dir.iterdir():
        if item.is_file() and item.name.endswith('.md'):
            print(f"- {item.name.replace('.md', '')}")

def indicate_deployed_path(file_name):
    """
    Indicates the expected path of a deployed prompt file.
    """
    current_working_dir = pathlib.Path.cwd()
    target_dir = current_working_dir / ".roo"
    target_file_path = target_dir / file_name
    print(f"Expected deployed path for '{file_name}': {target_file_path}")


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
    # Use files() for Python 3.9+ or files() from importlib_resources for older versions
    # Since pyproject.toml requires >=3.12, files() is built-in.
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy roo-conf prompts or list/locate them.")
    parser.add_argument(
        "-f", "--file",
        help="Specify a prompt file name (without .md extension) to locate its deployed path."
    )

    args = parser.parse_args()

    if args.file:
        indicate_deployed_path(args.file)
    elif len(sys.argv) == 1: # Check if no arguments were provided
         deploy_prompts()
    else: # If arguments other than --file were provided, list files
        list_available_prompts()