import pathlib
import platform
import json # Need json for reading/writing config, or pass config object/setter

def find_vscode_settings_paths():
    """
    Finds potential paths to custom_modes.yaml for VS Code and VS Code Insiders.
    Supports POSIX systems. Structure for future Windows extension.
    Returns a list of path strings.
    """
    home_dir = pathlib.Path.home()
    paths = []

    if platform.system() == "Linux" or platform.system() == "Darwin": # POSIX systems
        # VS Code path
        vscode_path = home_dir / ".vscode-server" / "data" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline" / "settings" / "custom_modes.yaml"
        if vscode_path.exists():
            paths.append(str(vscode_path))

        # VS Code Insiders path
        vscode_insiders_path = home_dir / ".vscode-server-insiders" / "data" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline" / "settings" / "custom_modes.yaml"
        if vscode_insiders_path.exists():
            paths.append(str(vscode_insiders_path))

    # TODO: Add Windows path finding logic here

    return paths

def manage_vscode_settings_paths(get_config_func, set_config_func):
    """
    Finds VS Code settings paths and stores them in the configuration if not already present.
    Returns a list of pathlib.Path objects for the settings files.
    """
    config = get_config_func()
    settings_files_str = config.get('vscode_settings_paths')

    if settings_files_str:
        print("Using stored settings paths from config.")
        settings_files = [pathlib.Path(p) for p in settings_files_str]
    else:
        print("Finding settings paths...")
        found_paths_str = find_vscode_settings_paths()
        if found_paths_str:
            # Store the found paths in the config
            set_config_func('vscode_settings_paths', found_paths_str)
            settings_files = [pathlib.Path(p) for p in found_paths_str]
        else:
            settings_files = []

    return settings_files