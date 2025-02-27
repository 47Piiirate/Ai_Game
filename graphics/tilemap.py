import pygame
import json
import os

class Tile:
    def __init__(self, image, tile_type="solid", properties=None):
        self.image = image
        self.type = tile_type  # solid, background, foreground, etc.
        self.properties = properties or {}

class TileMap:
    def __init__(self, tile_size=32):
        self.tile_size = tile_size
        self.tiles = {}  # Dictionary of tile types (by ID)
        self.layers = []  # List of layers, each is a 2D array of tile IDs
        self.width = 0
        self.height = 0
        self.collision_rects = []  # For collision detection
        self.spawn_points = {}  # Player and enemy spawn points
        self.transition_points = []  # Level transition points
        self.collectibles = []  # Collectible items
        
        # Parallax layers for background/foreground effects
        self.parallax_layers = []
    
    def load_tileset(self, tileset_path):
        """Load tile images from a tileset image"""
        try:
            # Load the tileset configuration
            with open(tileset_path + ".json", 'r') as f:
                tileset_data = json.load(f)
            
            # Load the tileset image
            tileset_image = pygame.image.load(tileset_path + ".png").convert_alpha()
            
            # Extract individual tiles
            for tile_id, tile_info in tileset_data["tiles"].items():
                tile_id = int(tile_id)
                x = (tile_id % tileset_data["columns"]) * self.tile_size
                y = (tile_id // tileset_data["columns"]) * self.tile_size
                
                # Cut out the tile from the tileset
                tile_image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
                tile_image.blit(tileset_image, (0, 0), (x, y, self.tile_size, self.tile_size))
                
                # Create tile with properties
                tile_type = tile_info.get("type", "solid")
                properties = tile_info.get("properties", {})
                self.tiles[tile_id] = Tile(tile_image, tile_type, properties)
                
        except Exception as e:
            print(f"Error loading tileset: {e}")
    
    def load_map(self, map_path):
        """Load a map from a JSON file (similar to Tiled format)"""
        try:
            with open(map_path, 'r') as f:
                map_data = json.load(f)
            
            self.width = map_data["width"]
            self.height = map_data["height"]
            
            # Load layers
            for layer_data in map_data["layers"]:
                if layer_data["type"] == "tilelayer":
                    # Convert 1D array to 2D for easier access
                    layer = []
                    for y in range(self.height):
                        row = []
                        for x in range(self.width):
                            index = y * self.width + x
                            if index < len(layer_data["data"]):
                                row.append(layer_data["data"][index])
                            else:
                                row.append(0)  # Empty tile
                        layer.append(row)
                    self.layers.append(layer)
                elif layer_data["type"] == "objectgroup":
                    self.load_objects(layer_data["objects"])
            
            # Build collision rects
            self.build_collision_rects()
            
        except Exception as e:
            print(f"Error loading map: {e}")
            # Create a basic fallback map
            self.create_default_map()
    
    def load_objects(self, objects):
        """Process object layers from the map"""
        for obj in objects:
            obj_type = obj.get("type", "")
            obj_rect = pygame.Rect(
                obj["x"], obj["y"],
                obj.get("width", self.tile_size),
                obj.get("height", self.tile_size)
            )
            
            if obj_type == "spawn":
                self.spawn_points["player"] = (obj["x"], obj["y"])
            elif obj_type == "enemy":
                enemy_type = obj.get("properties", {}).get("enemy_type", "basic")
                if "enemies" not in self.spawn_points:
                    self.spawn_points["enemies"] = []
                self.spawn_points["enemies"].append((obj["x"], obj["y"], enemy_type))
            elif obj_type == "transition":
                target_level = obj.get("properties", {}).get("target", "")
                spawn_x = obj.get("properties", {}).get("spawn_x", 0)
                spawn_y = obj.get("properties", {}).get("spawn_y", 0)
                self.transition_points.append((obj_rect, target_level, spawn_x, spawn_y))
            elif obj_type == "collectible":
                collectible_type = obj.get("properties", {}).get("type", "health")
                self.collectibles.append({"rect": obj_rect, "type": collectible_type})
    
    def build_collision_rects(self):
        """Create collision rectangles from the map tiles"""
        self.collision_rects = []
        
        # Assume first layer is the main collision layer
        if not self.layers:
            return
            
        layer = self.layers[0]
        
        # Scan each tile
        for y, row in enumerate(layer):
            for x, tile_id in enumerate(row):
                if tile_id > 0 and tile_id in self.tiles and self.tiles[tile_id].type == "solid":
                    self.collision_rects.append(pygame.Rect(
                        x * self.tile_size,
                        y * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    ))
    
    def create_default_map(self):
        """Create a simple default map if loading fails"""
        self.width = 40
        self.height = 20
        
        # Create a single layer with a floor and some platforms
        layer = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Add floor
        for x in range(self.width):
            layer[self.height - 1][x] = 1
        
        # Add some platforms
        for x in range(5, 10):
            layer[self.height - 5][x] = 1
            
        for x in range(15, 25):
            layer[self.height - 7][x] = 1
        
        self.layers.append(layer)
        
        # Create a basic tile for collision
        tile_image = pygame.Surface((self.tile_size, self.tile_size))
        tile_image.fill((100, 100, 100))
        self.tiles[1] = Tile(tile_image, "solid")
        
        # Build collision rectangles
        self.build_collision_rects()
        
        # Add spawn point
        self.spawn_points["player"] = (100, 100)
    
    def render(self, screen, camera_offset):
        """Render the map with camera offset"""
        # Calculate visible range based on camera position
        cam_x, cam_y = camera_offset
        start_x = max(0, cam_x // self.tile_size)
        start_y = max(0, cam_y // self.tile_size)
        end_x = min(self.width, (cam_x + screen.get_width()) // self.tile_size + 1)
        end_y = min(self.height, (cam_y + screen.get_height()) // self.tile_size + 1)
        
        # Render each layer
        for layer_index, layer in enumerate(self.layers):
            # Skip rendering for empty layers
            if not layer:
                continue
                
            for y in range(start_y, end_y):
                if y >= len(layer):
                    continue
                    
                for x in range(start_x, end_x):
                    if x >= len(layer[y]):
                        continue
                        
                    tile_id = layer[y][x]
                    if tile_id > 0 and tile_id in self.tiles:
                        # Calculate screen position
                        screen_x = x * self.tile_size - cam_x
                        screen_y = y * self.tile_size - cam_y
                        
                        # Draw the tile
                        screen.blit(self.tiles[tile_id].image, (screen_x, screen_y))
        
        # Debug: visualize collision rects and transition points
        for rect in self.collision_rects:
            debug_rect = rect.copy()
            debug_rect.x -= camera_offset[0]
            debug_rect.y -= camera_offset[1]
            pygame.draw.rect(screen, (255, 0, 0), debug_rect, 1)
        
        for transition_rect, _, _, _ in self.transition_points:
            debug_rect = transition_rect.copy()
            debug_rect.x -= camera_offset[0]
            debug_rect.y -= camera_offset[1]
            pygame.draw.rect(screen, (0, 255, 0), debug_rect, 1)
