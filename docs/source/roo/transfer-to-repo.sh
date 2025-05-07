#!/bin/bash

# Check if a repository path is provided
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <mode-slug> <path_to_git_repo>"
  return
fi

MODE_SLUG="$1"
REPO_PATH="$2"
TARGET_DIR="$REPO_PATH/.roo"
SOURCE_FILE="/home/mstouffer/.config/bash/roo/system-prompt-$MODE_SLUG"
TARGET_FILE="$TARGET_DIR/system-prompt-$MODE_SLUG"

# Create the .roo directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Copy the source file to the target directory
cp "$SOURCE_FILE" "$TARGET_FILE"

# Replace the {{repo-full-path}} token with the actual repo path
# Use sed -i to modify the file in place.
# Need to handle potential slashes in the path by using a different delimiter for sed, like '|'.
sed -i "s|{{repo-full-path}}|$REPO_PATH|g" "$TARGET_FILE"

echo "Successfully transferred and updated $SOURCE_FILE to $TARGET_FILE"
