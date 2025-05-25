import pathlib
import platform
import json # Need json for reading/writing config, or pass config object/setter

def find_vscode_settings_components():
    """
    Finds potential parent directories and relative paths for custom_modes.yaml
    for VS Code and VS Code Insiders.
    Supports POSIX systems. Structure for future Windows extension.
    Returns a list of dictionaries, each with 'parent_path' and 'relative_path'.
    """
    home_dir = pathlib.Path.home()
    components = []
    relative_path = pathlib.Path("settings") / "custom_modes.yaml"

    if platform.system() == "Linux" or platform.system() == "Darwin": # POSIX systems
        # VS Code path components
        vscode_parent = home_dir / ".vscode-server" / "data" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline"
        if (vscode_parent / relative_path).exists():
            components.append({
                'parent_path': str(vscode_parent),
                'relative_path': str(relative_path)
            })

        # VS Code Insiders path components
        vscode_insiders_parent = home_dir / ".vscode-server-insiders" / "data" / "User" / "globalStorage" / "rooveterinaryinc.roo-cline"
        if (vscode_insiders_parent / relative_path).exists():
            components.append({
                'parent_path': str(vscode_insiders_parent),
                'relative_path': str(relative_path)
            })

    # TODO: Add Windows path finding logic here

    return components

def manage_vscode_settings_paths(get_config_func, set_config_func):
    """
    Finds VS Code settings paths components and stores them in the configuration
    if not already present. Reconstructs and returns a list of pathlib.Path
    objects for the settings files.
    """
    config = get_config_func()
    settings_components = config.get('vscode_settings_components')

    if settings_components:
        print("Using stored settings path components from config.")
        settings_files = [pathlib.Path(item['parent_path']) / item['relative_path'] for item in settings_components]
    else:
        print("Finding settings path components...")
        found_components = find_vscode_settings_components()
        if found_components:
            # Store the found components in the config
            set_config_func('vscode_settings_components', found_components)
            settings_files = [pathlib.Path(item['parent_path']) / item['relative_path'] for item in found_components]
        else:
            settings_files = []

    # For backward compatibility, if old format exists and new doesn't, use old and convert
    if not settings_components:
        settings_files_str_old = config.get('vscode_settings_paths')
        if settings_files_str_old:
             print("Using old stored settings paths from config and converting.")
             settings_files = [pathlib.Path(p) for p in settings_files_str_old]
             # Attempt to convert and store in new format
             converted_components = []
             for full_path_str in settings_files_str_old:
                 full_path = pathlib.Path(full_path_str)
                 # This assumes the structure is always .../rooveterinaryinc.roo-cline/settings/custom_modes.yaml
                 # A more robust approach might be needed if the structure can vary
                 parts = full_path.parts
                 try:
                     settings_index = parts.index('settings')
                     parent_path = pathlib.Path(*parts[:settings_index])
                     relative_path = pathlib.Path(*parts[settings_index:])
                     converted_components.append({
                         'parent_path': str(parent_path),
                         'relative_path': str(relative_path)
                     })
                 except ValueError:
                     print(f"Warning: Could not parse path components for {full_path_str}")
                     # If parsing fails, we can't convert this path to the new format
                     pass
             if converted_components:
                 set_config_func('vscode_settings_components', converted_components)


    return settings_files

# TODO: Add functions for reading/writing custom_modes.yaml content