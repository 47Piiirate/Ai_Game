"""
Script to organize project files into a clear, modular structure
"""
import os
import shutil
import sys
from datetime import datetime

def create_directory_structure():
    """Create a clean directory structure for the game project"""
    
    # Define the directory structure
    directories = [
        "core",           # Core game mechanics
        "entities",       # Game entities (player, enemies, etc.)
        "systems",        # Game systems (animation, physics, etc.)
        "graphics",       # Graphics-related code
        "utils",          # Utility functions and helpers
        "assets/images/player",
        "assets/images/enemies",
        "assets/images/tiles",
        "assets/images/collectibles",
        "assets/images/ui",
        "docs",           # Documentation
        "tests",          # Tests
        "tools"           # Tools and scripts
    ]
    
    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create __init__.py files in Python module directories
    for directory in ["core", "entities", "systems", "graphics", "utils"]:
        init_file = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write(f'"""\n{directory.capitalize()} module for AI Game\n"""\n')
            print(f"Created {init_file}")

def organize_files():
    """Move files to their appropriate directories"""
    
    # Define files to move with their destinations
    file_moves = {
        # Core game files
        "app.py": "core/app.py",
        "game.py": "core/game.py",
        "level.py": "core/level.py",
        "game_state.py": "core/game_state.py",
        
        # Entity files
        "player.py": "entities/player.py",
        "enemy.py": "entities/enemy.py",
        "collectible.py": "entities/collectible.py",
        
        # System files
        "animation.py": "systems/animation.py",
        "camera.py": "systems/camera.py",
        "physics_engine.py": "systems/physics_engine.py",
        "achievements.py": "systems/achievements.py",
        
        # Graphics files
        "ui.py": "graphics/ui.py",
        "particles.py": "graphics/particles.py",
        
        # Utility files
        "asset_manager.py": "utils/asset_manager.py",
        "logger.py": "utils/logger.py",
        
        # Tool files
        "asset_loader.py": "tools/asset_loader.py",
        "asset_manager_patch.py": "tools/asset_manager_patch.py",
        "fix_enemy_render.py": "tools/fix_enemy_render.py",
        "check_dependencies.py": "tools/check_dependencies.py",
        
        # Rename files to more descriptive names
        "physics_engine.cpp": "systems/physics_engine.cpp",
    }
    
    # Create backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_organize_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    print(f"Created backup directory: {backup_dir}")
    
    # Move files
    for source, destination in file_moves.items():
        if os.path.exists(source):
            # Backup the file
            shutil.copy2(source, os.path.join(backup_dir, source))
            print(f"Backed up: {source}")
            
            # Create destination directory if needed
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            # Check if destination already exists
            if os.path.exists(destination):
                destination_backup = os.path.join(backup_dir, destination)
                os.makedirs(os.path.dirname(destination_backup), exist_ok=True)
                shutil.copy2(destination, destination_backup)
                print(f"Backed up existing destination: {destination}")
            
            # Copy file to new location
            shutil.copy2(source, destination)
            print(f"Moved: {source} -> {destination}")
            
            # Remove original file
            os.remove(source)

def update_imports():
    """Update import statements in all Python files to match the new structure"""
    
    # Define module mappings for imports
    module_mappings = {
        "app": "core.app",
        "game": "core.game",
        "level": "core.level",
        "game_state": "core.game_state",
        
        "player": "entities.player",
        "enemy": "entities.enemy",
        "collectible": "entities.collectible",
        
        "animation": "systems.animation",
        "camera": "systems.camera",
        "physics_engine": "systems.physics_engine",
        "achievements": "systems.achievements",
        
        "ui": "graphics.ui",
        "particles": "graphics.particles",
        
        "asset_manager": "utils.asset_manager",
        "logger": "utils.logger",
    }
    
    # Find all Python files
    python_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and not file == "organize_project.py":
                python_files.append(os.path.join(root, file))
    
    # Update imports in each file
    for file_path in python_files:
        with open(file_path, 'r') as f:
            content = f.read()
        
        updated_content = content
        
        # Update import statements
        for old_module, new_module in module_mappings.items():
            # Replace "from X import Y" style imports
            updated_content = updated_content.replace(f"from {old_module} import", f"from {new_module} import")
            
            # Replace "import X" style imports
            # Need to be careful with these to not replace partial matches
            updated_content = updated_content.replace(f"import {old_module}\n", f"import {new_module}\n")
            updated_content = updated_content.replace(f"import {old_module} ", f"import {new_module} ")
        
        # Write back the updated content if changed
        if updated_content != content:
            with open(file_path, 'w') as f:
                f.write(updated_content)
            print(f"Updated imports in: {file_path}")

def create_main_py():
    """Create a clean main.py entry point"""
    main_content = """# filepath: /s:/Learning/Python/Ai_Game/main.py
\"\"\"
AI Game - Main Entry Point
\"\"\"
import os
import pygame
import sys

# Set up environment
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"  # Hide pygame welcome message

def main():
    \"\"\"Main entry point for the game\"\"\"
    try:
        # Initialize pygame first
        pygame.init()
        
        # Then import our game modules
        from core.app import App
        from utils.logger import setup_logger
        from tools.check_dependencies import check_dependencies
        
        # Check dependencies
        check_dependencies()
        
        # Set up logging
        setup_logger()
        
        # Create and run application
        app = App()
        app.run()
        
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
"""
    
    # Create a backup of the existing main.py if it exists
    if os.path.exists("main.py"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"main.py.{timestamp}.bak"
        shutil.copy2("main.py", backup_file)
        print(f"Backed up existing main.py to {backup_file}")
    
    # Write the new main.py
    with open("main.py", "w") as f:
        f.write(main_content)
    print("Created new main.py entry point")

def update_readme():
    """Create/update a comprehensive README.md file"""
    readme_content = """# filepath: /s:/Learning/Python/Ai_Game/README.md
# AI Game Project

A 2D platformer game built with Pygame featuring animation, physics, collectibles and enemies.

## Overview

This game is a side-scrolling platformer with the following features:
- Smooth character movement and animation
- Physics-based platformer mechanics
- Enemy AI with basic behaviors
- Collectible items
- Camera system that follows the player
- UI elements

## Project Structure
"""
