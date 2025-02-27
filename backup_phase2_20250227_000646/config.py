"""
Game configuration settings
"""

# Asset directory structure
ASSET_DIR = "assets"
SPRITES_DIR = "Sprites"  # For backward compatibility
IMAGES_DIR = "images"
SOUNDS_DIR = "sounds"
MUSIC_DIR = "music"

# Asset subdirectories
PLAYER_SPRITES_DIR = "Characters/Heros/Main Hero"
ENEMY_SPRITES_DIR = "Characters/Enemies"
UI_SPRITES_DIR = "HUD"
TILESET_DIR = "Tileset"
VFX_DIR = "VFX"

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32

# Game settings
GRAVITY = 0.5
PLAYER_SPEED = 5
PLAYER_JUMP = 10
PLAYER_MAX_HEALTH = 100

# Debug settings
DEBUG = True
SHOW_FPS = True
SHOW_HITBOXES = False

# Audio settings
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7

def get_asset_path(asset_type, filename):
    """
    Get the correct path for an asset file
    
    Args:
        asset_type: Type of asset ("image", "sound", "music")
        filename: Name of the file
        
    Returns:
        Path to the asset file
    """
    import os
    
    if asset_type == "image":
        return os.path.join(ASSET_DIR, IMAGES_DIR, filename)
    elif asset_type == "sound":
        return os.path.join(ASSET_DIR, SOUNDS_DIR, filename)
    elif asset_type == "music":
        return os.path.join(ASSET_DIR, MUSIC_DIR, filename)
    elif asset_type == "sprite":
        return os.path.join(ASSET_DIR, SPRITES_DIR, filename)
    else:
        return os.path.join(ASSET_DIR, filename)
