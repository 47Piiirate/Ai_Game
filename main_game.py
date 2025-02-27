import pygame
from asset_manager import load_assets

# Initialize Pygame
pygame.init()

# Load assets
assets = load_assets()

# Check if any asset failed to load
for asset_name, asset in assets.items():
    if asset is None:
        print(f"Failed to load asset: {asset_name}")

# Example of creating a game object with a loaded image
hero_image = assets["hero_complete_sheet"]
if hero_image:
    hero_rect = hero_image.get_rect()
    # ...existing code...
else:
    print("Error: Hero image not loaded, cannot create hero object")

# ...existing code...
