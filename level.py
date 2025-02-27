import pygame
import json
import os

class Level:
    def __init__(self, asset_manager=None):
        self.tiles = []
        self.background_layers = []
        self.foreground_layers = []
        self.transition_points = []
        self.current_area = None
        self.areas = {}  # Dictionary of level areas
        self.collectibles = []
        self.asset_manager = asset_manager
        self.tile_image = None
        
        # Load the tile image if asset manager is available
        if self.asset_manager:
            self.tile_image = self.asset_manager.get_image("tile/tile")
        
        self.load_level("starting_area")
    
    def load_level(self, level_name):
        self.current_area = level_name
        self.tiles = []
        self.transition_points = []  # Reset to empty list
        self.collectibles = []
        
        # In a real game, you would load this from a JSON or Tiled map file
        # For this example, we'll create some predefined level layouts
        if level_name == "starting_area":
            self.create_starting_area()
        elif level_name == "underground_cave":
            self.create_underground_cave()
        elif level_name == "boss_chamber":
            self.create_boss_chamber()
        
        # Load background images (in a real game)
        # self.load_background_layers(level_name)
    
    def create_starting_area(self):
        # Create a simple starting area
        tile_size = 40
        
        # Floor
        for x in range(0, 1280, tile_size):
            tile = pygame.Rect(x, 500, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Platforms
        for x in range(200, 400, tile_size):
            tile = pygame.Rect(x, 350, tile_size, tile_size)
            self.tiles.append(tile)
        
        for x in range(600, 900, tile_size):
            tile = pygame.Rect(x, 400, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Walls
        for y in range(300, 500, tile_size):
            # Left wall
            tile = pygame.Rect(0, y, tile_size, tile_size)
            self.tiles.append(tile)
            # Right wall
            tile = pygame.Rect(1240, y, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Add transition to underground cave - make it more visible
        transition = pygame.Rect(1160, 420, 80, 80)
        # Store as tuple (rect, target_level, spawn_x, spawn_y) 
        self.transition_points.append((transition, "underground_cave", 50, 400))
        
        # Add a collectible
        self.collectibles.append({
            "rect": pygame.Rect(500, 450, 20, 20),
            "type": "health"
        })
    
    def create_underground_cave(self):
        # Create an underground cave area
        tile_size = 40
        
        # Floor
        for x in range(0, 1280, tile_size):
            tile = pygame.Rect(x, 500, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Ceiling
        for x in range(0, 1280, tile_size):
            tile = pygame.Rect(x, 100, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Platforms with gaps for challenging jumps
        for x in range(200, 300, tile_size):
            tile = pygame.Rect(x, 350, tile_size, tile_size)
            self.tiles.append(tile)
        
        for x in range(400, 500, tile_size):
            tile = pygame.Rect(x, 400, tile_size, tile_size)
            self.tiles.append(tile)
        
        for x in range(600, 700, tile_size):
            tile = pygame.Rect(x, 350, tile_size, tile_size)
            self.tiles.append(tile)
        
        for x in range(800, 900, tile_size):
            tile = pygame.Rect(x, 400, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Walls
        for y in range(100, 500, tile_size):
            # Left wall
            tile = pygame.Rect(0, y, tile_size, tile_size)
            self.tiles.append(tile)
            # Right wall
            tile = pygame.Rect(1240, y, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Add transition back to starting area - make it more visible
        transition = pygame.Rect(0, 420, 40, 80)
        self.transition_points.append((transition, "starting_area", 1150, 400))
        
        # Add transition to boss chamber (needs a special ability to access)
        transition = pygame.Rect(1200, 420, 40, 80)
        self.transition_points.append((transition, "boss_chamber", 50, 400))
        
        # Add collectibles
        self.collectibles.append({
            "rect": pygame.Rect(650, 300, 20, 20),
            "type": "ability_double_jump"
        })
    
    def create_boss_chamber(self):
        # Create a boss chamber area
        tile_size = 40
        
        # Floor
        for x in range(0, 1280, tile_size):
            tile = pygame.Rect(x, 550, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Ceiling
        for x in range(0, 1280, tile_size):
            tile = pygame.Rect(x, 50, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Walls
        for y in range(50, 550, tile_size):
            # Left wall
            tile = pygame.Rect(0, y, tile_size, tile_size)
            self.tiles.append(tile)
            # Right wall
            tile = pygame.Rect(1240, y, tile_size, tile_size)
            self.tiles.append(tile)
        
        # Add transition back to underground cave
        transition = pygame.Rect(0, 470, 40, 80)
        self.transition_points.append((transition, "underground_cave", 1150, 400))
    
    def check_transitions(self, player_rect):
        for transition_rect, target_level, spawn_x, spawn_y in self.transition_points:
            if player_rect.colliderect(transition_rect):
                return (target_level, spawn_x, spawn_y)
        return None
    
    def render(self, screen, camera_offset):
        # Render background layers
        for layer in self.background_layers:
            # Parallax scrolling would be implemented here
            pass
        
        # Render tiles
        for tile in self.tiles:
            # Apply camera offset
            tile_rect = tile.copy()
            tile_rect.x -= camera_offset[0]
            tile_rect.y -= camera_offset[1]
            
            if self.tile_image:
                screen.blit(self.tile_image, tile_rect)
            else:
                pygame.draw.rect(screen, (100, 100, 100), tile_rect)
        
        # Render transition points with a visible indicator
        for transition, target_level, _, _ in self.transition_points:
            transition_rect = transition.copy()
            transition_rect.x -= camera_offset[0]
            transition_rect.y -= camera_offset[1]
            pygame.draw.rect(screen, (0, 255, 0), transition_rect, 4)  # Make transitions more visible
            
            # Add a subtle animation to make it more noticeable
            inner_rect = transition_rect.copy()
            inner_rect.inflate_ip(-8, -8)
            pygame.draw.rect(screen, (0, 200, 0), inner_rect, 2) 
        
        # Render collectibles
        for collectible in self.collectibles:
            collectible_rect = collectible["rect"].copy()
            collectible_rect.x -= camera_offset[0]
            collectible_rect.y -= camera_offset[1]
            
            # Different colors for different types
            if collectible["type"] == "health":
                color = (255, 0, 0)  # Red for health
            elif collectible["type"].startswith("ability_"):
                color = (0, 255, 255)  # Cyan for abilities
            else:
                color = (255, 255, 0)  # Yellow default
                
            pygame.draw.rect(screen, color, collectible_rect)
            # Add a slight glow effect
            pygame.draw.rect(screen, (255, 255, 255), collectible_rect, 1)
        
        # Render foreground layers
        for layer in self.foreground_layers:
            # Parallax scrolling would be implemented here
            pass
