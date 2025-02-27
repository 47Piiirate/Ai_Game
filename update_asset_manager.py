"""
Update the asset_manager.py to a simplified version that focuses only on images
and has improved error handling
"""
import os

# Define the new asset manager content as a proper string
NEW_ASSET_MANAGER = '''import os
import pygame

class AssetManager:
    def __init__(self):
        self.images = {}
        self.initialized = False
        print("Asset Manager initialized")
    
    def initialize(self):
        """Initialize pygame if not already done"""
        if not pygame.get_init():
            pygame.init()
        self.initialized = True
    
    def load_image(self, path):
        """Load an image and return a pygame surface or a fallback if it fails."""
        if not self.initialized:
            self.initialize()
            
        # Check if image was already loaded
        if path in self.images:
            return self.images[path]
        
        try:
            full_path = os.path.join(os.path.dirname(__file__), path)
            
            # Check if file exists
            if not os.path.exists(full_path):
                print(f"Warning: Image file does not exist: {full_path}")
                # Return a fallback image (small colored square)
                fallback = pygame.Surface((32, 32), pygame.SRCALPHA)
                fallback.fill((255, 0, 255))  # Magenta for visibility
                pygame.draw.line(fallback, (0, 0, 0), (0, 0), (32, 32), 2)
                pygame.draw.line(fallback, (0, 0, 0), (32, 0), (0, 32), 2)
                self.images[path] = fallback
                return fallback
            
            # Try to load the image
            image = pygame.image.load(full_path).convert_alpha()
            self.images[path] = image
            return image
                
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Return a fallback image (small colored square)
            fallback = pygame.Surface((32, 32), pygame.SRCALPHA)
            fallback.fill((255, 0, 255))  # Magenta for visibility
            pygame.draw.line(fallback, (0, 0, 0), (0, 0), (32, 32), 2)
            pygame.draw.line(fallback, (0, 0, 0), (32, 0), (0, 32), 2)
            self.images[path] = fallback
            return fallback
    
    def load_sprite_sheet(self, path, width, height, frames, spacing=0):
        """Load a sprite sheet and split it into individual frames."""
        try:
            sheet = self.load_image(path)
            sprite_frames = []
            
            for i in range(frames):
                x = i * (width + spacing)
                frame = pygame.Surface((width, height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (x, 0, width, height))
                sprite_frames.append(frame)
            
            return sprite_frames
        except Exception as e:
            print(f"Error loading sprite sheet {path}: {e}")
            # Return fallback frames
            return [self.create_fallback_image() for _ in range(frames)]
    
    def create_fallback_image(self, width=32, height=32):
        """Create a fallback image when loading fails."""
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.fill((255, 0, 255))  # Magenta for visibility
        pygame.draw.line(image, (0, 0, 0), (0, 0), (width, height), 2)
        pygame.draw.line(image, (0, 0, 0), (width, 0), (0, height), 2)
        return image

    def preload_images(self, paths):
        """Preload multiple images at once"""
        for path in paths:
            self.load_image(path)
        print(f"Preloaded {len(paths)} images")
'''

def update_asset_manager():
    """Create simplified version of asset_manager.py"""
    file_path = "asset_manager.py"
    
    # Backup current file if it exists
    if os.path.exists(file_path):
        backup_path = file_path + ".old"
        print(f"Backing up current asset_manager.py to {backup_path}")
        with open(file_path, 'r') as src:
            with open(backup_path, 'w') as dst:
                dst.write(src.read())
    
    # Write new asset manager
    print("Writing simplified asset_manager.py")
    with open(file_path, 'w') as f:
        f.write(NEW_ASSET_MANAGER)
    
    print("Asset manager updated successfully")

if __name__ == "__main__":
    update_asset_manager()
