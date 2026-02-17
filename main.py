"""
File Renamer Utility
====================
This module automates bulk renaming of files within a specified directory.

It converts all filenames to title case and replaces a user-defined character
(or substring) with a new one. Only files whose names contain the old character
are reported in the output, making it easy to audit what changed.

Usage:
    python rename_files.py <target_directory>

Arguments:
    target_directory (str): The path to the directory whose files will be renamed.
                            Passed as the first command-line argument via sys.argv.

Example:
    python rename_files.py /home/user/photos
    > Enter the old char you want to change: _
    > Enter the new char: -
    > my_photo_01.jpg => My-Photo-01.Jpg

Notes:
    - Filenames are title-cased BEFORE the character replacement is applied,
      so the old character should match the case as it appears after title-casing.
    - This script renames ALL files in the directory, not just those containing
      the old character. Files without the old character are still title-cased.
    - Subdirectories inside the target directory are also renamed since
      os.listdir() returns both files and folders.
"""

import os
from sys import argv

# ── Configuration ─────────────────────────────────────────────────────────────

# Retrieve the target directory from the first command-line argument.
# Example: python rename_files.py /path/to/dir
parent_dir = argv[1]

# Change the current working directory to the target directory.
# This ensures relative path operations inside the loop resolve correctly.
os.chdir(parent_dir)

# Prompt the user for the substring to find and its replacement.
old_char = input("Enter the old char you want to change: ")
new_char = input("Enter the new char: ")

# ── Renaming Loop ─────────────────────────────────────────────────────────────

for file in os.listdir(parent_dir):
    old_name = file  # Preserve the original filename for comparison and reporting.

    # Apply title case first, then replace the target character/substring.
    # title() capitalises the first letter of each word in the filename.
    new_name = file.title().replace(old_char, new_char)

    # Build absolute paths so os.rename() works regardless of the cwd.
    old_full_name = os.path.join(parent_dir, old_name)
    new_full_name = os.path.join(parent_dir, new_name)

    # Perform the actual rename on disk.
    os.rename(old_full_name, new_full_name)

    # Only log files where a substitution actually occurred, keeping output clean.
    if old_char in old_name:
        print(f"{old_name} => {new_name}")
