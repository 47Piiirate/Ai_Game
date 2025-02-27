class Camera:
    def __init__(self, screen_width, screen_height):
        self.x = 0
        self.y = 0
        self.width = screen_width
        self.height = screen_height
        self.target_x = 0
        self.target_y = 0
        self.smoothing = 0.1  # Camera smoothing factor
    
    def update(self, player):
        # Calculate target position (center player on screen)
        self.target_x = player.rect.centerx - (self.width / 2)
        self.target_y = player.rect.centery - (self.height / 2)
        
        # Apply smooth camera movement
        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing
        
        # Clamp camera position to prevent showing outside the level
        # In a real game, you would clamp to the level boundaries
        self.x = max(0, min(self.x, 2000 - self.width))
        self.y = max(0, min(self.y, 1000 - self.height))
    
    def get_offset(self):
        return (int(self.x), int(self.y))
