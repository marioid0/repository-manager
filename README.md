# repository-manager

A simple CLI tool to organize files into folders by `[tag]`, built using Python's `os`, `re`, `shutil`, and `argparse`.

> This program was developed as part of my learning during the Google Data Analytics course, to test my skills in analyzing and organizing files based on tags.

### Features

- Scans directories for files containing `[tag]` in their names.
- Groups files by extension inside a `[tag]`-named folder.
- Simulates or actually moves files.
- Easy CLI interface.

### Example

```bash
# Dry-run preview
python gestor.py show manufacturing --source ./input --dry-run

# Organize files by tag
python gestor.py process manufacturing --source ./input --target ./gestor
