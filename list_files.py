import os
import sys
from pathlib import Path
import argparse

def list_files(directory, recursive=True, extensions=None, include_hidden=False):
    """
    List all files in the given directory
    
    Args:
        directory: Path to directory
        recursive: Whether to include subdirectories
        extensions: List of file extensions to include (e.g. ['.py', '.txt'])
        include_hidden: Whether to include hidden files
    """
    # Ensure directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory.")
        return
        
    # Initialize counters
    file_count = 0
    dir_count = 0
    
    print(f"\nListing files in: {os.path.abspath(directory)}")
    print("=" * 80)
    
    # Walk through directory
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories if not include_hidden
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # Get relative path from base directory
        rel_path = os.path.relpath(root, directory)
        if rel_path == ".":
            rel_path = ""
        
        # Print directory name
        if rel_path:
            print(f"\n📁 {rel_path}/")
            dir_count += 1
        else:
            print("\n📁 ./")
        
        # Print files
        for file in sorted(files):
            # Skip hidden files if not include_hidden
            if not include_hidden and file.startswith('.'):
                continue
                
            # Check file extension if specified
            if extensions and not any(file.endswith(ext) for ext in extensions):
                continue
                
            file_path = os.path.join(rel_path, file)
            full_path = os.path.join(root, file)
            file_size = os.path.getsize(full_path)
            
            # Format file size
            if file_size < 1024:
                size_str = f"{file_size} B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size/1024:.1f} KB"
            else:
                size_str = f"{file_size/(1024*1024):.1f} MB"
                
            print(f"  📄 {file:<30} {size_str:>10}")
            file_count += 1
        
        # Stop recursion if not recursive
        if not recursive:
            break
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"Total: {file_count} files in {dir_count} directories")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List files in a directory")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to list files from")
    parser.add_argument("-r", "--recursive", action="store_true", help="List files recursively")
    parser.add_argument("-e", "--extensions", help="Filter by extensions (comma separated, e.g. .py,.txt)")
    parser.add_argument("-a", "--all", action="store_true", help="Include hidden files")
    
    args = parser.parse_args()
    
    # Parse extensions if provided
    extensions = None
    if args.extensions:
        extensions = args.extensions.split(',')
        # Ensure extensions start with a dot
        extensions = [ext if ext.startswith('.') else '.' + ext for ext in extensions]
    
    list_files(args.directory, args.recursive, extensions, args.all)
