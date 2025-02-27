import pygame

class Minimap:
    """Minimap system for displaying player position and explored areas"""
    def __init__(self, world_width, world_height, minimap_size=150):
        self.world_width = world_width
        self.world_height = world_height
        self.minimap_size = minimap_size
        
        # Create minimap surface
        self.surface = pygame.Surface((minimap_size, minimap_size), pygame.SRCALPHA)
        
        # Color settings
        self.background_color = (0, 0, 0, 150)  # Semi-transparent black
        self.border_color = (255, 255, 255)
        self.player_color = (255, 0, 0)  # Red for player
        self.explored_color = (100, 100, 100)  # Gray for explored areas
        self.current_area_color = (150, 150, 150)  # Lighter gray for current area
        self.special_areas = {
            "save_point": (0, 255, 0),  # Green for save points
            "boss_room": (255, 0, 0),   # Red for boss rooms
            "item_room": (0, 0, 255),   # Blue for item rooms
        }
        
        # Map data
        self.explored_rooms = set()  # Set of room IDs that have been explored
        self.rooms = {}  # Dictionary of room data by ID
        self.current_room = None  # ID of current room
        
        # Position and state
        self.position = (20, 20)  # Top-left corner position
        self.is_expanded = False  # Whether showing expanded view
        self.expand_size = (300, 200)  # Size when expanded
    
    def add_room(self, room_id, pos, size, room_type="normal"):
        """Add a room to the minimap"""
        self.rooms[room_id] = {
            "pos": pos,  # (x, y) in world coordinates
            "size": size,  # (width, height) in world coordinates
            "type": room_type,  # Room type for coloring
            "connections": []  # List of connected room IDs
        }
    
    def add_connection(self, room_id1, room_id2):
        """Add a connection between two rooms"""
        if room_id1 in self.rooms and room_id2 in self.rooms:
            if room_id2 not in self.rooms[room_id1]["connections"]:
                self.rooms[room_id1]["connections"].append(room_id2)
            if room_id1 not in self.rooms[room_id2]["connections"]:
                self.rooms[room_id2]["connections"].append(room_id1)
    
    def mark_room_explored(self, room_id):
        """Mark a room as explored"""
        if room_id in self.rooms:
            self.explored_rooms.add(room_id)
    
    def set_current_room(self, room_id):
        """Set the current room"""
        if room_id in self.rooms:
            self.current_room = room_id
            self.mark_room_explored(room_id)  # Automatically mark as explored
    
    def toggle_expand(self):
        """Toggle between normal and expanded view"""
        self.is_expanded = not self.is_expanded
    
    def _world_to_minimap(self, x, y):
        """Convert world coordinates to minimap coordinates"""
        map_size = self.expand_size if self.is_expanded else (self.minimap_size, self.minimap_size)
        
        # Scale to minimap size
        map_x = (x / self.world_width) * map_size[0]
        map_y = (y / self.world_height) * map_size[1]
        
        return map_x, map_y
    
    def _room_rect_on_minimap(self, room):
        """Get a room's rectangle in minimap coordinates"""
        pos_x, pos_y = self._world_to_minimap(room["pos"][0], room["pos"][1])
        size_x, size_y = self._world_to_minimap(room["size"][0], room["size"][1])
        
        # Ensure minimum size for visibility
        size_x = max(3, size_x)
        size_y = max(3, size_y)
        
        return pygame.Rect(pos_x, pos_y, size_x, size_y)
    
    def render(self, screen, player_pos):
        """Render the minimap to the screen"""
        if self.is_expanded:
            self._render_expanded(screen, player_pos)
        else:
            self._render_normal(screen, player_pos)
    
    def _render_normal(self, screen, player_pos):
        """Render normal (small) minimap"""
        # Clear minimap surface
        self.surface.fill(self.background_color)
        
        # Draw explored rooms
        for room_id in self.explored_rooms:
            room = self.rooms.get(room_id)
            if room:
                rect = self._room_rect_on_minimap(room)
                color = self.current_area_color if room_id == self.current_room else self.explored_color
                
                # Use special color if applicable
                if room["type"] in self.special_areas:
                    color = self.special_areas[room["type"]]
                
                pygame.draw.rect(self.surface, color, rect)
                
                # Draw connections to explored rooms
                for connected_id in room["connections"]:
                    if connected_id in self.explored_rooms:
                        connected_room = self.rooms.get(connected_id)
                        if connected_room:
                            start_rect = self._room_rect_on_minimap(room)
                            end_rect = self._room_rect_on_minimap(connected_room)
                            
                            start_pos = (start_rect.centerx, start_rect.centery)
                            end_pos = (end_rect.centerx, end_rect.centery)
                            
                            pygame.draw.line(self.surface, self.explored_color, start_pos, end_pos, 1)
        
        # Draw player position
        player_x, player_y = self._world_to_minimap(player_pos[0], player_pos[1])
        pygame.draw.circle(self.surface, self.player_color, (int(player_x), int(player_y)), 2)
        
        # Draw border
        pygame.draw.rect(self.surface, self.border_color, (0, 0, self.minimap_size, self.minimap_size), 1)
        
        # Draw to screen at position
        screen.blit(self.surface, self.position)
    
    def _render_expanded(self, screen, player_pos):
        """Render expanded (large) minimap with more details"""
        # Create expanded surface
        expanded = pygame.Surface(self.expand_size, pygame.SRCALPHA)
        expanded.fill((0, 0, 0, 200))  # Darker background for expanded view
        
        # Draw title
        font = pygame.font.Font(None, 24)
        title = font.render("Map", True, (255, 255, 255))
        expanded.blit(title, (10, 10))
        
        # Draw room labels and more detailed connections
        # (Similar to normal render but with more details)
        
        # Draw all rooms (including unexplored but visible from explored rooms)
        visible_rooms = set(self.explored_rooms)
        
        # Add rooms connected to explored rooms
        for room_id in self.explored_rooms:
            for connected_id in self.rooms.get(room_id, {}).get("connections", []):
                visible_rooms.add(connected_id)
        
        # First draw connections
        for room_id in self.explored_rooms:
            room = self.rooms.get(room_id)
            if room:
                for connected_id in room["connections"]:
                    if connected_id in self.explored_rooms:
                        connected_room = self.rooms.get(connected_id)
                        if connected_room:
                            start_rect = self._room_rect_on_minimap(room)
                            end_rect = self._room_rect_on_minimap(connected_room)
                            
                            start_pos = (start_rect.centerx, start_rect.centery)
                            end_pos = (end_rect.centerx, end_rect.centery)
                            
                            pygame.draw.line(expanded, (100, 100, 100), start_pos, end_pos, 2)
        
        # Then draw rooms
        for room_id in visible_rooms:
            room = self.rooms.get(room_id)
            if room:
                rect = self._room_rect_on_minimap(room)
                
                # Different appearance based on explored status
                if room_id in self.explored_rooms:
                    color = self.current_area_color if room_id == self.current_room else self.explored_color
                    
                    # Use special color if applicable
                    if room["type"] in self.special_areas:
                        color = self.special_areas[room["type"]]
                    
                    pygame.draw.rect(expanded, color, rect)
                    
                    # Draw room name for explored rooms
                    if self.is_expanded:
                        label = font.render(f"Room {room_id}", True, (255, 255, 255))
                        expanded.blit(label, (rect.x, rect.y - 15))
                else:
                    # Unexplored but visible rooms
                    pygame.draw.rect(expanded, (50, 50, 50), rect)
        
        # Draw player
        player_x, player_y = self._world_to_minimap(player_pos[0], player_pos[1])
        pygame.draw.circle(expanded, self.player_color, (int(player_x), int(player_y)), 4)
        
        # Draw border
        pygame.draw.rect(expanded, self.border_color, (0, 0, self.expand_size[0], self.expand_size[1]), 2)
        
        # Position in center of screen
        center_x = screen.get_width() // 2 - self.expand_size[0] // 2
        center_y = screen.get_height() // 2 - self.expand_size[1] // 2
        screen.blit(expanded, (center_x, center_y))
