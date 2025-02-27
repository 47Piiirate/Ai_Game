"""
Phase 2 of the game cleanup process:
Organizing the core game structure
"""
import os
import shutil
import sys
from datetime import datetime

# Setup backup directory with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = f"backup_phase2_{timestamp}"
os.makedirs(backup_dir, exist_ok=True)
print(f"Created backup directory: {backup_dir}")

# Define the core directory structure
directories = [
    "core",
    "entities",
    "systems",
    "graphics",
    "utils",
    "assets/images/player",
    "assets/images/enemies",
    "assets/images/tiles",
    "assets/images/collectibles",
    "assets/images/ui"
]

# Create directory structure
print("Creating directory structure...")
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

# Define files to move to each directory
file_moves = {
    "core": ["app.py", "game.py", "game_state.py", "config.py"],
    "entities": ["player.py", "enemy.py", "npc.py", "collectible.py"],
    "systems": ["animation.py", "physics.py", "camera.py", "achievements.py", "inventory.py", 
                "combat_manager.py", "quest_system.py", "save_manager.py"],
    "graphics": ["tilemap.py", "particles.py", "ui.py", "minimap.py"],
    "utils": ["asset_manager.py", "asset_loader.py", "logger.py"]
}

# Create __init__.py files for each module
print("\nCreating __init__.py files...")
for directory in directories:
    if not directory.startswith("assets"):
        init_file = os.path.join(directory, "__init__.py")
        with open(init_file, "w") as f:
            f.write(f'"""\n{directory.capitalize()} module for AI Game\n"""\n')
        print(f"Created: {init_file}")

# Function to backup and move a file
def backup_and_move(source, dest_dir):
    if os.path.exists(source):
        # Make backup
        backup_path = os.path.join(backup_dir, source)
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(source, backup_path)
        
        # Create destination path
        dest_path = os.path.join(dest_dir, os.path.basename(source))
        
        # Move file
        print(f"Moving {source} to {dest_path}")
        try:
            # Read original content
            with open(source, 'r') as f:
                content = f.read()
            
            # Write to destination
            with open(dest_path, 'w') as f:
                f.write(content)
                
            # Remove original
            os.remove(source)
            
            return True
        except Exception as e:
            print(f"Error moving {source}: {e}")
            return False
    else:
        print(f"File not found: {source}")
        return False

# Move files to their new directories
print("\nMoving files to appropriate directories...")
for dest_dir, files in file_moves.items():
    for file in files:
        backup_and_move(file, dest_dir)

# Update import statements in moved files
print("\nUpdating import statements in moved files...")
for directory, files in file_moves.items():
    for file in files:
        file_path = os.path.join(directory, os.path.basename(file))
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Update imports based on new structure
            new_content = content
            
            for src_dir, src_files in file_moves.items():
                for src_file in src_files:
                    base_name = os.path.splitext(os.path.basename(src_file))[0]
                    
                    # Replace direct imports
                    old_import = f"from {base_name} import"
                    new_import = f"from {src_dir}.{base_name} import"
                    new_content = new_content.replace(old_import, new_import)
                    
                    # Replace import statements
                    old_import = f"import {base_name}"
                    new_import = f"import {src_dir}.{base_name} as {base_name}"
                    new_content = new_content.replace(old_import + "\n", new_import + "\n")
                    new_content = new_content.replace(old_import + " ", new_import + " ")
            
            # Write updated content
            with open(file_path, 'w') as f:
                f.write(new_content)
                
        except Exception as e:
            print(f"Error updating imports in {file_path}: {e}")

# Update main.py to use the new import structure
main_file = "main.py"
try:
    with open(main_file, 'r') as f:
        content = f.read()
        
    # Update app import
    content = content.replace("from app import App", "from core.app import App")
    
    with open(main_file, 'w') as f:
        f.write(content)
    
    print(f"Updated imports in main.py")
except Exception as e:
    print(f"Error updating main.py: {e}")

print("\nPhase 2 cleanup complete!")
print(f"1. Files were backed up to: {backup_dir}")
print(f"2. Directory structure created")
print(f"3. Files moved to appropriate directories")
print(f"4. Import statements updated")
print("\nNext step: Test that the game runs correctly with 'python main.py'")
