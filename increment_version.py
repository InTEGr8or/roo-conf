import tomlkit
import sys

def increment_patch_version(version):
    """Increments the patch version of a semantic version string."""
    try:
        parts = list(map(int, version.split('.')))
        if len(parts) < 3:
            # Assume patch is missing, add .0 and increment
            parts = parts + [0] * (3 - len(parts))
        parts[-1] += 1
        return ".".join(map(str, parts))
    except ValueError:
        print(f"Error: Could not parse version string '{version}'", file=sys.stderr)
        sys.exit(1)

def main():
    pyproject_path = "pyproject.toml"
    try:
        with open(pyproject_path, "r") as f:
            doc = tomlkit.parse(f.read())

        current_version = doc["project"]["version"]
        new_version = increment_patch_version(current_version)

        doc["project"]["version"] = new_version

        with open(pyproject_path, "w") as f:
            f.write(tomlkit.dumps(doc))

        print(f"Version incremented from {current_version} to {new_version}")

    except FileNotFoundError:
        print(f"Error: {pyproject_path} not found.", file=sys.stderr)
        sys.exit(1)
    except KeyError:
        print(f"Error: 'project.version' not found in {pyproject_path}.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()