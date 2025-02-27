"""
Tool to check and create the correct asset directory structure
"""

import os
from logger import get_logger

logger = get_logger()

def check_asset_structure():
    """
    Check if the asset directory structure is correct and create any missing directories
    
    Returns:
        bool: True if the structure was correct or successfully created, False otherwise
    """
    required_directories = [
        "assets",
        "assets/images",
        "assets/images/player",
        "assets/images/enemies",
        "assets/images/tiles",
        "assets/images/ui",
        "assets/images/collectibles",
        "assets/sounds",
        "assets/music",
        "assets/Sprites",
        "assets/Sprites/Characters/Heros/Main Hero",
        "assets/Sprites/Characters/Enemies",
        "assets/Sprites/HUD",
        "assets/Sprites/Tileset",
        "assets/Sprites/VFX"
    ]
    
    try:
        for directory in required_directories:
            # Convert path to system-specific format
            directory = directory.replace("/", os.sep)
            
            # Check if directory exists, create if not
            if not os.path.exists(directory):
                logger.info(f"Creating directory: {directory}")
                os.makedirs(directory)
        
        logger.info("Asset directory structure is complete")
        return True
    except Exception as e:
        logger.error(f"Error checking/creating asset directory structure: {e}")
        return False

def create_default_readme_files():
    """
    Create default README files in asset directories to explain their purpose
    """
    readme_files = {
        "assets/images/player/README.txt": 
            "This directory contains player character sprites and animations.\n"
            "Required files:\n"
            "- player.png: Main character sprite\n"
            "- player_idle.png: Idle animation\n"
            "- player_run.png: Running animation\n"
            "- player_jump.png: Jump animation\n",
        
        "assets/images/enemies/README.txt": 
            "This directory contains enemy sprites and animations.\n"
            "Required files:\n"
            "- enemy.png: Basic enemy sprite\n"
            "- boss.png: Boss enemy sprite\n"
            "- drone.png: Flying enemy\n"
            "- police.png: Authority enemy\n"
            "- guard.png: Security guard\n",
        
        "assets/sounds/README.txt":
            "This directory contains sound effects for the game.\n"
            "Required files:\n"
            "- jump.wav: Jump sound effect\n"
            "- dash.wav: Dash sound\n"
            "- attack.wav: Attack sound\n"
            "- hit.wav: Hit/damage sound\n"
            "- collect.wav: Collectible pickup sound\n",
        
        "assets/music/README.txt":
            "This directory contains music tracks for the game.\n"
            "Required files:\n"
            "- title_theme.mp3: Title screen music\n"
            "- main_area.mp3: Main area background music\n"
            "- boss.mp3: Boss fight music\n"
    }
    
    try:
        for file_path, content in readme_files.items():
            # Convert path to system-specific format
            file_path = file_path.replace("/", os.sep)
            
            # Create directory if it doesn't exist
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            # Skip if file already exists
            if os.path.exists(file_path):
                continue
            
            # Create the README file
            with open(file_path, 'w') as f:
                f.write(content)
        
        logger.info("Default README files created")
        return True
    except Exception as e:
        logger.error(f"Error creating README files: {e}")
        return False

if __name__ == "__main__":
    check_asset_structure()
    create_default_readme_files()
