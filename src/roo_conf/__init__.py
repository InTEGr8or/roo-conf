import argparse
import os
import json
from pathlib import Path
import sys

def hello() -> str:
    return "Hello from roo-conf!"

def extract_conversations_command(args):
    """Extracts conversation history from VS Code global storage."""
    target_repo_path = Path(args.target_repo_path).resolve()
    print(f"Extracting conversations for repository: {target_repo_path}")

    vscode_storage_paths = [
        Path.home() / ".vscode-server" / "data" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline",
        Path.home() / ".vscode-server-insiders" / "data" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline",
        Path.home() / ".config" / "Code" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline", # Linux path for VS Code
        Path.home() / ".config" / "Code - Insiders" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline", # Linux path for VS Code Insiders
        Path.home() / "Library" / "Application Support" / "Code" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline", # macOS path for VS Code
        Path.home() / "Library" / "Application Support" / "Code - Insiders" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline", # macOS path for VS Code Insiders
        Path(os.getenv("APPDATA", "")) / "Code" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline", # Windows path for VS Code
        Path(os.getenv("APPDATA", "")) / "Code - Insiders" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline", # Windows path for VS Code Insiders
    ]

    task_history = []
    found_global_state_file = None

    # Search for a JSON file containing "taskHistory" within the known storage paths
    for storage_path in vscode_storage_paths:
        if storage_path.exists():
            print(f"Searching in: {storage_path}")
            for root, _, files in os.walk(storage_path):
                for file in files:
                    if file.endswith(".json"):
                        file_path = Path(root) / file
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if '"taskHistory"' in content:
                                    print(f"Found potential global state file: {file_path}")
                                    found_global_state_file = file_path
                                    break # Assume the first one found is correct
                        except Exception as e:
                            # Report error but continue searching
                            print(f"Error reading {file_path}: {e}", file=sys.stderr)
                if found_global_state_file:
                    break
        if found_global_state_file:
            break

    if not found_global_state_file:
        print("Error: Could not find the global state file containing task history in known VS Code storage locations.", file=sys.stderr)
        return

    try:
        with open(found_global_state_file, 'r', encoding='utf-8') as f:
            global_state_data = json.load(f)
            task_history = global_state_data.get("taskHistory", [])
            print(f"Found {len(task_history)} task history items in global state.")
    except FileNotFoundError:
        # This should ideally not happen after finding the file, but included for robustness
        print(f"Error: Global state file not found at {found_global_state_file}", file=sys.stderr)
        return
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from global state file at {found_global_state_file}. File might be corrupted or in an unexpected format.", file=sys.stderr)
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading global state file {found_global_state_file}: {e}", file=sys.stderr)
        return

    extracted_count = 0
    errors_encountered = []
    output_dir = target_repo_path / ".roo-conf" / "conversations"

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error: Could not create output directory {output_dir}: {e}", file=sys.stderr)
        return

    for item in task_history:
        # Validate essential fields in history item
        if not isinstance(item, dict):
            errors_encountered.append(f"Skipping invalid history item (not a dictionary): {item}")
            continue

        workspace_path_str = item.get("workspace")
        task_id = item.get("taskId")

        if not workspace_path_str:
            errors_encountered.append(f"Skipping history item with no workspace field: {item}")
            continue

        if not task_id:
            errors_encountered.append(f"Skipping history item with no taskId: {item}")
            continue

        try:
            workspace_path = Path(workspace_path_str).resolve()
        except Exception as e:
            errors_encountered.append(f"Skipping history item with invalid workspace path '{workspace_path_str}': {e}")
            continue

        if workspace_path == target_repo_path:
            conversation_dir = found_global_state_file.parent / str(task_id)
            api_history_path = conversation_dir / "api_conversation_history.json"
            ui_messages_path = conversation_dir / "ui_messages.json"

            if not api_history_path.exists():
                errors_encountered.append(f"Skipping task {task_id}: API history file not found at {api_history_path}")
                continue
            if not ui_messages_path.exists():
                errors_encountered.append(f"Skipping task {task_id}: UI messages file not found at {ui_messages_path}")
                continue

            try:
                with open(api_history_path, 'r', encoding='utf-8') as f:
                    api_history = json.load(f)
                with open(ui_messages_path, 'r', encoding='utf-8') as f:
                    ui_messages = json.load(f)

                markdown_content = convert_to_markdown(api_history, ui_messages)

                # Generate a simple filename for now, can improve later
                # Ensure filename is safe
                safe_task_id = "".join(c for c in str(task_id) if c.isalnum() or c in ('-', '_')).rstrip()
                if not safe_task_id:
                     safe_task_id = "unknown_task"

                filename = f"conversation_{safe_task_id}.md"
                output_path = output_dir / filename

                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    extracted_count += 1
                    print(f"Extracted conversation {task_id} to {output_path}")
                except Exception as e:
                    errors_encountered.append(f"Error writing conversation {task_id} to {output_path}: {e}")


            except FileNotFoundError:
                # This should ideally not happen due to the exists() check, but included for robustness
                errors_encountered.append(f"Error: Conversation files not found for task {task_id}")
            except json.JSONDecodeError:
                errors_encountered.append(f"Error: Could not parse JSON for task {task_id}. Files might be corrupted or in an unexpected format.")
            except Exception as e:
                errors_encountered.append(f"An unexpected error occurred while processing task {task_id}: {e}")

    print(f"\nFinished extracting conversations.")
    print(f"Total conversations found for repository: {extracted_count}")
    print(f"Extracted conversations saved to: {output_dir}")


    if errors_encountered:
        print("\nErrors encountered during extraction:", file=sys.stderr)
        for error in errors_encountered:
            print(f"- {error}", file=sys.stderr)


def convert_to_markdown(api_history, ui_messages):
    """Converts API history and UI messages into a Markdown string."""
    markdown_output = "# Conversation\n\n"

    # Assuming a simple turn structure where API history and UI messages correspond
    # This might need refinement based on actual data structure

    # Sort messages by timestamp if timestamps are available and reliable
    # For now, interleave based on index as a basic approach

    # Create a combined list of messages with a source indicator
    combined_messages = []
    for msg in ui_messages:
        combined_messages.append({"source": "user", "timestamp": msg.get("timestamp"), "content": msg.get("message")})
    for msg in api_history:
         combined_messages.append({"source": "assistant", "timestamp": msg.get("timestamp"), "content": msg.get("content")})

    # Attempt to sort by timestamp if timestamps are present in all messages
    try:
        if all(msg.get("timestamp") is not None for msg in combined_messages):
             # Assuming timestamp is in a sortable format (e.g., ISO 8601 string or number)
            combined_messages.sort(key=lambda x: x.get("timestamp"))
        else:
            # Fallback to interleaving if timestamps are missing or inconsistent
            print("Warning: Timestamps missing or inconsistent, falling back to interleaving messages by index.", file=sys.stderr)
            combined_messages = []
            max_len = max(len(api_history), len(ui_messages))
            for i in range(max_len):
                if i < len(ui_messages):
                    combined_messages.append({"source": "user", "timestamp": ui_messages[i].get("timestamp"), "content": ui_messages[i].get("message")})
                if i < len(api_history):
                    combined_messages.append({"source": "assistant", "timestamp": api_history[i].get("timestamp"), "content": api_history[i].get("content")})

    except Exception as e:
        print(f"Error sorting messages by timestamp: {e}. Falling back to interleaving.", file=sys.stderr)
        combined_messages = []
        max_len = max(len(api_history), len(ui_messages))
        for i in range(max_len):
            if i < len(ui_messages):
                combined_messages.append({"source": "user", "timestamp": ui_messages[i].get("timestamp"), "content": ui_messages[i].get("message")})
            if i < len(api_history):
                combined_messages.append({"source": "assistant", "timestamp": api_history[i].get("timestamp"), "content": api_history[i].get("content")})


    for msg in combined_messages:
        role = "User" if msg["source"] == "user" else "Assistant"
        timestamp = msg.get("timestamp", "N/A")
        content = msg.get("content", "N/A")

        markdown_output += f"## {role} ({timestamp})\n\n"
        markdown_output += f"{content}\n\n"

    return markdown_output


def main():
    parser = argparse.ArgumentParser(description="roo-conf CLI tool")
    subparsers = parser.add_subparsers(dest="command")

    # Add extract-conversations command
    extract_parser = subparsers.add_parser("extract-conversations", help="Extract conversation history from VS Code global storage")
    extract_parser.add_argument(
        "target_repo_path",
        nargs="?", # Make the argument optional
        default=".", # Default to current working directory
        help="Path to the target repository (defaults to current working directory)"
    )
    extract_parser.set_defaults(func=extract_conversations_command)

    # Add existing parsers from deploy.py if needed in the future
    # from . import deploy
    # deploy.add_subparser(subparsers)


    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
