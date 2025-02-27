"""
Phase 1 of the game cleanup process:
Identifying and removing redundant files
"""
import os
import shutil
from datetime import datetime

# Create backup directory with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = f"backup_{timestamp}"
os.makedirs(backup_dir, exist_ok=True)

def backup_file(filepath):
    """Backup a file to the backup directory"""
    if os.path.exists(filepath):
        relative_path = os.path.dirname(filepath)
        backup_path = os.path.join(backup_dir, relative_path)
        os.makedirs(backup_path, exist_ok=True)
        dest_path = os.path.join(backup_dir, filepath)
        print(f"Backing up: {filepath} → {dest_path}")
        shutil.copy2(filepath, dest_path)
        return True
    return False

def remove_file(filepath):
    """Backup and remove a file"""
    if backup_file(filepath):
        print(f"Removing: {filepath}")
        os.remove(filepath)
        return True
    else:
        print(f"File not found, skipping: {filepath}")
        return False

# 1. Remove redundant launcher files
launcher_files = [
    "game_launcher.py",
    "launch_game.py", 
    "run_game.bat", 
    "main_game.py"
]

print("=== Removing Redundant Launcher Files ===")
for file in launcher_files:
    remove_file(file)

# 2. Consolidate asset management
asset_management_files = [
    "asset_manager.py.bak",
    "asset_manager_patch.py", 
    "debug_asset_manager.py",
    "image_loading_tracer.py", 
    "debug_image_loading.py"
]

print("\n=== Consolidating Asset Management Files ===")
for file in asset_management_files:
    remove_file(file)

# 3. Clean up utility scripts
utility_scripts = [
    "test_pygame.py", 
    "snake_game.py",
    "debug_game_init.py", 
    "check_python.py",
    "create_placeholder_sounds.py", 
    "create_sound_directories.py"
]

print("\n=== Removing Utility Scripts ===")
for file in utility_scripts:
    remove_file(file)

# 4. Consolidate fix scripts
fix_scripts = [
    "fix_check.py", 
    "fix_game_issues.py", 
    "complete_game_fix.py",
    "DEBUG_README.md", 
    "FIX_README.md"
]

print("\n=== Removing Fix Scripts ===")
for file in fix_scripts:
    remove_file(file)

# Remove sound-related files and example sounds
sound_files = [
    "sound_manager.py",
    "sound_effects.py",
    "boom.wav", 
    "car_door.wav", 
    "found.wav", 
    "missing.wav", 
    "punch.wav", 
    "whiff.wav"
]

print("\n=== Removing Sound-Related Files ===")
for file in sound_files:
    remove_file(file)

# Remove example sprites
example_sprites = [
    "chimp.png", 
    "fist.png", 
    "liquid.bmp"
]

print("\n=== Removing Example Sprites ===")
for file in example_sprites:
    remove_file(file)

# Create a summary of removed files
with open("cleanup_summary.txt", "w") as f:
    f.write(f"Cleanup Phase 1 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 50 + "\n\n")
    
    f.write("Removed Launcher Files:\n")
    f.write("\n".join([f"- {file}" for file in launcher_files]) + "\n\n")
    
    f.write("Removed Asset Management Files:\n")
    f.write("\n".join([f"- {file}" for file in asset_management_files]) + "\n\n")
    
    f.write("Removed Utility Scripts:\n")
    f.write("\n".join([f"- {file}" for file in utility_scripts]) + "\n\n")
    
    f.write("Removed Fix Scripts:\n")
    f.write("\n".join([f"- {file}" for file in fix_scripts]) + "\n\n")
    
    f.write("Removed Sound-Related Files:\n")
    f.write("\n".join([f"- {file}" for file in sound_files]) + "\n\n")
    
    f.write("Removed Example Sprites:\n")
    f.write("\n".join([f"- {file}" for file in example_sprites]) + "\n\n")
    
    f.write("\nAll files were backed up to the directory: " + backup_dir)

print(f"\nPhase 1 cleanup complete. All removed files were backed up to: {backup_dir}")
print(f"Summary written to: cleanup_summary.txt")
