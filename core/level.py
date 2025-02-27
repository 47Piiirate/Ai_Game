import pygame

class Level:
    """Level management and rendering"""
    
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
        self.platforms = []
        self.background = None
        self.width = 2000  # Level width (larger than screen)
        self.height = 1000  # Level height
        
        # Create a basic level with floor and some platforms
        self._create_default_level()
    
    def _create_default_level(self):
        """Create a default level with some platforms"""
        # Main floor
        floor = pygame.Rect(0, 550, self.width, 50)
        self.platforms.append(floor)
        
        # Some platforms
        plat1 = pygame.Rect(200, 400, 200, 20)
        plat2 = pygame.Rect(500, 300, 200, 20)
        plat3 = pygame.Rect(800, 350, 200, 20)
        
        self.platforms.extend([plat1, plat2, plat3])
        
        # Try to load background
        try:
            self.background = self.asset_manager.load_image("assets/images/tiles/background.png")
        except:
            # Create a simple gradient background
            self.background = pygame.Surface((self.width, self.height))
            for y in range(self.height):
                # Create a gradient from dark blue to black
                color = (0, 0, max(0, 50 - y // 10))
                pygame.draw.line(self.background, color, (0, y), (self.width, y))
    
    def get_platforms(self):
        """Return the list of platforms for collision detection"""
        return self.platforms
    
    def render(self, screen, camera_offset=(0, 0)):
        """Render the level with camera offset"""
        # Draw background
        if self.background:
            # Only draw visible portion of background
            view_rect = pygame.Rect(camera_offset[0], camera_offset[1], 
                                   screen.get_width(), screen.get_height())
            screen.blit(self.background, (0, 0), view_rect)
        
        # Draw platforms
        for platform in self.platforms:
            # Apply camera offset
            platform_rect = pygame.Rect(
                platform.x - camera_offset[0],
                platform.y - camera_offset[1],
                platform.width,
                platform.height
            )
            
            # Only draw if on screen
            if (platform_rect.right > 0 and platform_rect.left < screen.get_width() and
                platform_rect.bottom > 0 and platform_rect.top < screen.get_height()):
                pygame.draw.rect(screen, (100, 100, 100), platform_rect)
                pygame.draw.rect(screen, (50, 50, 50), platform_rect, 2)  # Border
    
    def check_collision(self, entity_rect):
        """Check if an entity collides with any platform"""
        collisions = []
        for platform in self.platforms:
            if entity_rect.colliderect(platform):
                collisions.append(platform)
        return collisions
