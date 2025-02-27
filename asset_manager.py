"""
Asset Manager to handle loading and caching of game assets
"""
import os
import pygame
import math  # Add this import for math.cos and math.sin

class AssetManager:
    def __init__(self):
        # Create cache dictionaries
        self.images = {}
        self.animations = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}
        
        # Base asset paths
        self.base_path = "assets"
        self.image_path = os.path.join(self.base_path, "images")
        self.sound_path = os.path.join(self.base_path, "sounds") 
        self.music_path = os.path.join(self.base_path, "music")
        self.font_path = os.path.join(self.base_path, "fonts")
        
        # Ensure directories exist
        os.makedirs(self.image_path, exist_ok=True)
        os.makedirs(self.sound_path, exist_ok=True)
        os.makedirs(self.music_path, exist_ok=True)
        os.makedirs(self.font_path, exist_ok=True)
        
        # Create subdirectories for better organization
        self.player_path = os.path.join(self.image_path, "player")
        self.enemy_path = os.path.join(self.image_path, "enemies")
        self.tile_path = os.path.join(self.image_path, "tiles")
        self.ui_path = os.path.join(self.image_path, "ui")
        self.collectible_path = os.path.join(self.image_path, "collectibles")
        
        os.makedirs(self.player_path, exist_ok=True)
        os.makedirs(self.enemy_path, exist_ok=True)
        os.makedirs(self.tile_path, exist_ok=True) 
        os.makedirs(self.ui_path, exist_ok=True)
        os.makedirs(self.collectible_path, exist_ok=True)
        
        # Create placeholder assets if needed
        self._create_placeholder_assets()
    
    def _create_placeholder_assets(self):
        """Create basic placeholder assets if they don't exist"""
        # Player placeholder
        player_file = os.path.join(self.player_path, "player.png")
        if not os.path.exists(player_file):
            surface = pygame.Surface((50, 50))
            surface.fill((255, 0, 0))  # Red player
            pygame.draw.rect(surface, (200, 0, 0), (10, 10, 30, 30))  # Body
            pygame.draw.circle(surface, (255, 200, 200), (25, 15), 8)  # Head
            pygame.image.save(surface, player_file)
            print(f"Created placeholder player image at {player_file}")
        
        # Enemy placeholder
        enemy_file = os.path.join(self.enemy_path, "enemy.png")
        if not os.path.exists(enemy_file):
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            surface.fill((0, 0, 255, 200))  # Blue enemy
            pygame.draw.polygon(surface, (0, 0, 200), [(10, 40), (25, 10), (40, 40)])  # Triangle
            pygame.image.save(surface, enemy_file)
            print(f"Created placeholder enemy image at {enemy_file}")
            
        # Boss placeholder
        boss_file = os.path.join(self.enemy_path, "boss.png")
        if not os.path.exists(boss_file):
            surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            surface.fill((255, 0, 255, 200))  # Purple boss
            pygame.draw.circle(surface, (200, 0, 200), (50, 50), 40)  # Body
            pygame.draw.circle(surface, (255, 255, 0), (40, 40), 10)  # Left eye
            pygame.draw.circle(surface, (255, 255, 0), (60, 40), 10)  # Right eye
            pygame.image.save(surface, boss_file)
            print(f"Created placeholder boss image at {boss_file}")
        
        # Tile placeholder
        tile_file = os.path.join(self.tile_path, "tile.png")
        if not os.path.exists(tile_file):
            surface = pygame.Surface((40, 40))
            surface.fill((100, 100, 100))  # Gray tile
            pygame.draw.rect(surface, (50, 50, 50), (0, 0, 40, 40), 2)  # Border
            pygame.draw.line(surface, (70, 70, 70), (0, 0), (40, 40), 1)
            pygame.draw.line(surface, (70, 70, 70), (0, 40), (40, 0), 1)
            pygame.image.save(surface, tile_file)
            print(f"Created placeholder tile image at {tile_file}")
        
        # Collectible placeholders
        for collectible_type in ["health", "dash", "double_jump", "wall_jump", "charged_attack"]:
            collectible_file = os.path.join(self.collectible_path, f"{collectible_type}.png")
            if not os.path.exists(collectible_file):
                surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                if collectible_type == "health":
                    surface.fill((255, 0, 0, 200))  # Red for health
                    pygame.draw.rect(surface, (255, 255, 255), (8, 2, 4, 16))  # Cross
                    pygame.draw.rect(surface, (255, 255, 255), (2, 8, 16, 4))  # Cross
                elif collectible_type == "dash":
                    surface.fill((255, 0, 255, 200))  # Purple for dash
                    pygame.draw.polygon(surface, (255, 255, 255), [(2, 10), (15, 5), (15, 15)])  # Arrow
                elif collectible_type == "double_jump":
                    surface.fill((0, 255, 0, 200))  # Green for double jump
                    pygame.draw.polygon(surface, (255, 255, 255), [(10, 2), (5, 10), (15, 10)])  # Up arrow
                    pygame.draw.polygon(surface, (255, 255, 255), [(10, 18), (5, 10), (15, 10)])  # Down arrow
                elif collectible_type == "wall_jump":
                    surface.fill((0, 0, 255, 200))  # Blue for wall jump
                    pygame.draw.rect(surface, (255, 255, 255), (2, 2, 4, 16))  # Wall
                    pygame.draw.polygon(surface, (255, 255, 255), [(8, 10), (18, 5), (18, 15)])  # Arrow
                else:  # charged_attack
                    surface.fill((255, 255, 0, 200))  # Yellow for charged attack
                    pygame.draw.circle(surface, (255, 255, 255), (10, 10), 5)  # Center
                    for i in range(8):
                        angle = i * math.pi / 4.0  # Use math.pi
                        # Use math.cos and math.sin instead of pygame.math.cos and pygame.math.sin
                        x = 10 + 8 * math.cos(angle)
                        y = 10 + 8 * math.sin(angle)
                        pygame.draw.line(surface, (255, 255, 255), (10, 10), (int(x), int(y)), 2)
                pygame.image.save(surface, collectible_file)
                print(f"Created placeholder collectible image at {collectible_file}")

    def get_image(self, name, scale=None):
        """Load an image, applying optional scaling"""
        # First check if it's already cached
        cache_key = f"{name}_{scale}"
        if cache_key in self.images:
            return self.images[cache_key]
        
        # Determine file path based on name
        if name.startswith("player/"):
            path = os.path.join(self.player_path, name.replace("player/", ""))
        elif name.startswith("enemy/"):
            path = os.path.join(self.enemy_path, name.replace("enemy/", ""))
        elif name.startswith("tile/"):
            path = os.path.join(self.tile_path, name.replace("tile/", ""))
        elif name.startswith("ui/"):
            path = os.path.join(self.ui_path, name.replace("ui/", ""))
        elif name.startswith("collectible/"):
            path = os.path.join(self.collectible_path, name.replace("collectible/", ""))
        else:
            path = os.path.join(self.image_path, name)
        
        # Add extension if needed
        if not path.endswith((".png", ".jpg", ".bmp")):
            path += ".png"
        
        try:
            image = pygame.image.load(path).convert_alpha()
            
            # Apply scaling if specified
            if scale:
                if isinstance(scale, (tuple, list)) and len(scale) == 2:
                    image = pygame.transform.scale(image, scale)
                elif isinstance(scale, (int, float)):
                    w, h = image.get_size()
                    new_w, new_h = int(w * scale), int(h * scale)
                    image = pygame.transform.scale(image, (new_w, new_h))
            
            # Cache the image
            self.images[cache_key] = image
            return image
        except pygame.error:
            print(f"Error loading image: {path}")
            
            # Create a placeholder image
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 255))  # Magenta for missing textures
            pygame.draw.line(placeholder, (0, 0, 0), (0, 0), (50, 50), 2)
            pygame.draw.line(placeholder, (0, 0, 0), (0, 50), (50, 0), 2)
            
            self.images[cache_key] = placeholder
            return placeholder
    
    def get_sound(self, name):
        """Load a sound effect"""
        if name in self.sounds:
            return self.sounds[name]
        
        path = os.path.join(self.sound_path, name)
        
        # Add extension if needed
        if not path.endswith((".wav", ".ogg", ".mp3")):
            path += ".wav"
        
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
            return sound
        except pygame.error:
            print(f"Error loading sound: {path}")
            return None
    
    def get_music(self, name):
        """Get path to music file"""
        path = os.path.join(self.music_path, name)
        
        # Add extension if needed
        if not path.endswith((".mp3", ".wav", ".ogg")):
            path += ".mp3"
        
        if os.path.exists(path):
            return path
        else:
            print(f"Error: Music file not found: {path}")
            return None
