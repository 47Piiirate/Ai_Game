import os
import pygame
import sys

class AssetManager:
    def __init__(self):
        self.images = {}
        self.initialized = False
        print("Asset Manager initialized")
        
        # Store the project root path
        self.project_root = self._get_project_root()
        print(f"Project root: {self.project_root}")
    
    def _get_project_root(self):
        """Get the absolute path to the project root directory"""
        # Get the absolute path of this file
        this_file = os.path.abspath(__file__)
        
        # Go up two directories (from utils/ to project root)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
        
        # If we're in the wrong location, try to find the actual project root
        if not os.path.exists(os.path.join(project_root, "main.py")):
            # Try to find from current working directory
            cwd = os.getcwd()
            if os.path.exists(os.path.join(cwd, "main.py")):
                project_root = cwd
        
        return project_root
    
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
            # Construct full path from project root
            full_path = os.path.join(self.project_root, path)
            
            # Print path for debugging
            print(f"Loading image from: {full_path}")
            
            # Check if file exists
            if not os.path.exists(full_path):
                print(f"Warning: Image file does not exist: {full_path}")
                fallback = self.create_fallback_image()
                self.images[path] = fallback
                return fallback
            
            # Try to load the image
            image = pygame.image.load(full_path).convert_alpha()
            self.images[path] = image
            return image
                
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            fallback = self.create_fallback_image()
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
            return [self.create_fallback_image(width, height) for _ in range(frames)]
    
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
