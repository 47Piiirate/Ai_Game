import pygame
import os

pygame.init()
print("Pygame initialized successfully")
print(f"Pygame version: {pygame.version.ver}")

# Test directory structure 
print("\nChecking asset directories...")
directories = [
    "assets",
    "assets/images",
    "assets/images/player",
    "assets/images/enemies",
    "assets/images/tiles",
    "assets/images/collectibles",
    "assets/sounds",
    "assets/music"
]

for directory in directories:
    if os.path.exists(directory):
        print(f"✓ {directory} exists")
    else:
        print(f"✗ {directory} missing")

print("\nGame should be ready to run!")
