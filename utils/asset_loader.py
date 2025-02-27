"""
Helper tool to copy assets from a source folder to the game's asset structure
"""
import os
import shutil
import sys

def copy_assets(source_folder, target_folder="assets"):
    """
    Copy assets from source folder to the game's asset structure
    
    Args:
        source_folder: Path to the folder containing assets
        target_folder: Path to the game's asset folder (default: 'assets')
    """
    # Ensure target directories exist
    os.makedirs(os.path.join(target_folder, "images", "player"), exist_ok=True)  # Player images
    os.makedirs(os.path.join(target_folder, "images", "enemies"), exist_ok=True)  # Enemy images
    os.makedirs(os.path.join(target_folder, "images", "tiles"), exist_ok=True)  # Tile images
    os.makedirs(os.path.join(target_folder, "images", "ui"), exist_ok=True)  # UI images
    os.makedirs(os.path.join(target_folder, "images", "collectibles"), exist_ok=True)  # Collectible images
    os.makedirs(os.path.join(target_folder, "sounds"), exist_ok=True)  # Sound effects
    os.makedirs(os.path.join(target_folder, "music"), exist_ok=True)  # Music tracks

    
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return
    
    # Get all files in source folder (including subdirectories)
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            
            # Determine target directory based on file extension
            if file.endswith((".png", ".jpg", ".bmp", ".gif")):
                # Images
                if "player" in file.lower():
                    target_dir = os.path.join(target_folder, "images", "player")
                elif "enemy" in file.lower() or "boss" in file.lower():
                    target_dir = os.path.join(target_folder, "images", "enemies")
                elif "tile" in file.lower() or "block" in file.lower():
                    target_dir = os.path.join(target_folder, "images", "tiles")
                elif "ui" in file.lower() or "button" in file.lower() or "menu" in file.lower():
                    target_dir = os.path.join(target_folder, "images", "ui")
                elif "item" in file.lower() or "pickup" in file.lower() or "collect" in file.lower():
                    target_dir = os.path.join(target_folder, "images", "collectibles")
                else:
                    target_dir = os.path.join(target_folder, "images")  # Default images directory

            elif file.endswith((".wav", ".ogg")) and not ("music" in root.lower() or "soundtrack" in root.lower()):
                # Sound effects
                target_dir = os.path.join(target_folder, "sounds")
            elif file.endswith((".mp3", ".wav")) and ("music" in root.lower() or "soundtrack" in root.lower()):
                # Music
                target_dir = os.path.join(target_folder, "music")
            else:
                # Skip other file types
                continue
            
            # Copy file to target directory
            target_path = os.path.join(target_dir, file)
            print(f"Copying {source_path} -> {target_path}")
            shutil.copy2(source_path, target_path)
    
    print("Asset import complete!")

if __name__ == "__main__":
    # Get source folder from command line argument or ask user
    if len(sys.argv) > 1:
        source_folder = sys.argv[1]
    else:
        source_folder = input("Enter path to folder containing assets: ")
    
    copy_assets(source_folder)
