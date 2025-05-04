#!/usr/bin/env python3
"""
gestor.py - CLI to organize files by [tag].

Commands:
  show     Show a preview of how files will be organized.
  process  Move files into a structured folder based on [tag].

Usage:
  python gestor.py show <tag> --source ./input --dry-run
  python gestor.py process <tag> --source ./input --target ./gestor
"""

import os
import re
import shutil
import argparse


def extract_tag(filename):
    """Extracts the first [tag] from a filename."""
    match = re.search(r'\[([^\[\]]+)\]', filename)
    return match.group(1) if match else None


def scan_dir(source, tag):
    """
    Scans 'source' for files containing [tag] in their name.
    Returns a dictionary mapping file extensions to file paths.
    """
    ext_map = {}
    for root, _, files in os.walk(source):
        for filename in files:
            if f'[{tag}]' in filename:
                ext = filename.rsplit('.', 1)[-1] if '.' in filename else ''
                ext_map.setdefault(ext, []).append(os.path.join(root, filename))
    return ext_map


def print_tree(ext_map, tag):
    """Prints a tree-like structure of how files will be organized."""
    print('/gestor')
    print(f'└── [{tag}]')
    exts = sorted(ext_map.keys())
    for i, ext in enumerate(exts):
        branch = '├──' if i < len(exts) - 1 else '└──'
        print(f'    {branch} {ext}/')
        for path in sorted(ext_map[ext]):
            print(f'        └── {os.path.basename(path)}')


def move_files(ext_map, tag, target, dry_run):
    """
    Moves or simulates moving files into folders by extension under the [tag] folder.
    """
    base_path = os.path.join(target, f'[{tag}]')
    for ext, files in ext_map.items():
        dest_dir = os.path.join(base_path, ext)
        os.makedirs(dest_dir, exist_ok=True)
        for src in files:
            dst = os.path.join(dest_dir, os.path.basename(src))
            if dry_run:
                print(f'[dry-run] mv "{src}" -> "{dst}"')
            else:
                shutil.move(src, dst)
                print(f'✓ mv "{src}" -> "{dst}"')


def main():
    parser = argparse.ArgumentParser(description='Organize files by [tag].')
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    # Show command
    show_p = subparsers.add_parser('show', help='Show how files will be organized.')
    show_p.add_argument('tag', help='Tag to search for (without brackets).')
    show_p.add_argument('--source', '-s', default='.', help='Source directory.')
    show_p.add_argument('--dry-run', action='store_true', help='Simulate the process.')

    # Process command
    proc_p = subparsers.add_parser('process', help='Organize and move files.')
    proc_p.add_argument('tag', help='Tag to search for (without brackets).')
    proc_p.add_argument('--source', '-s', default='.', help='Source directory.')
    proc_p.add_argument('--target', '-t', default='./gestor', help='Target directory.')
    proc_p.add_argument('--dry-run', action='store_true', help='Simulate the process.')

    args = parser.parse_args()

    ext_map = scan_dir(args.source, args.tag)
    print_tree(ext_map, args.tag)

    if args.cmd == 'process':
        proceed = args.dry_run or input('Proceed? (Y/n): ').strip().lower() in ('', 'y')
        if proceed:
            move_files(ext_map, args.tag, args.target, args.dry_run)


if __name__ == '__main__':
    main()
