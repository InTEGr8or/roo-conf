# Implementation Task List for roo-conf (Fix .git in List)

This file outlines the task to fix the inclusion of the .git directory when listing available prompts from a remote source.

## Tasks:

- Modify the `list_available_prompts` function in `src/roo_conf/deploy.py` to exclude the `.git` directory and its contents when iterating through files in the local templates directory (`~/.config/roo-conf/templates`).
- Ensure that only actual template files (e.g., markdown files) are listed from the remote source.
- Update documentation (if necessary) to reflect this fix.