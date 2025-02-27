import os
import sys
import pygame
from pprint import pprint
import traceback

def analyze_asset_manager():
    """Attempt to import and analyze the asset manager class"""
    try:
        from asset_manager import AssetManager
        print("Successfully imported AssetManager class")
        
        # Create an instance with debug mode
        asset_mgr = AssetManager(debug=True)
        print("Successfully created AssetManager instance")
        
        # Return the asset manager for further inspection
        return asset_mgr
    except Exception as e:
        print(f"Error analyzing AssetManager: {e}")
        traceback.print_exc()
        return None

def debug_image_loading():
    """Debug function to check all images in the Sprites directory and potential asset paths."""
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    # Dictionary to store results
    results = {
        "successful": [],
        "failed": []
    }
    
    # Common directories to check
    dirs_to_check = [
        "Sprites",
        "sprites",
        "assets/images",
        "Assets/Images",
        "images"
    ]
    
    for base_dir in dirs_to_check:
        sprites_dir = os.path.join(os.path.dirname(__file__), base_dir)
        if not os.path.exists(sprites_dir):
            print(f"Directory not found: {sprites_dir}")
            continue
            
        print(f"Checking directory: {sprites_dir}")
        
        # Walk through all files in the directory
        for root, _, files in os.walk(sprites_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, os.path.dirname(__file__))
                    
                    try:
                        img = pygame.image.load(full_path)
                        if img is None:
                            results["failed"].append({
                                "path": relative_path,
                                "error": "Image loaded as None"
                            })
                        else:
                            try:
                                rect = img.get_rect()
                                results["successful"].append({
                                    "path": relative_path,
                                    "size": rect.size
                                })
                            except Exception as e:
                                results["failed"].append({
                                    "path": relative_path,
                                    "error": f"get_rect() failed: {str(e)}"
                                })
                    except Exception as e:
                        results["failed"].append({
                            "path": relative_path,
                            "error": str(e)
                        })
    
    return results

def print_file_structure():
    """Prints the directory structure to help with debugging path issues"""
    print("\n=== DIRECTORY STRUCTURE ===\n")
    
    # Print the current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Walk through the project directory and print structure
    project_dir = os.path.dirname(__file__)
    for root, dirs, files in os.walk(project_dir):
        level = root.replace(project_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        
        # Print directories first
        for d in dirs:
            if not d.startswith(('.', '__')) and d != "__pycache__":  # Skip hidden dirs and pycache
                print(f"{sub_indent}{d}/")
        
        # Print files
        for f in files:
            if not f.startswith(('.', '__')) and not f.endswith(('.pyc')):  # Skip hidden files and pyc
                print(f"{sub_indent}{f}")

if __name__ == "__main__":
    print("\n=== ASSET MANAGER DEBUGGER ===\n")
    
    # Print file structure
    print_file_structure()
    
    # Analyze AssetManager class
    asset_mgr = analyze_asset_manager()
    
    # Check image loading
    results = debug_image_loading()
    
    print("\n=== DEBUG IMAGE LOADING RESULTS ===\n")
    print(f"Total images checked: {len(results['successful']) + len(results['failed'])}")
    print(f"Successful: {len(results['successful'])}")
    print(f"Failed: {len(results['failed'])}")
    
    if results['failed']:
        print("\n=== FAILED IMAGES ===")
        pprint(results['failed'])
    
    pygame.quit()
    
    print("\nDebugging complete. See results above for issues that need to be fixed.")
