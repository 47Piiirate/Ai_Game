import pygame
from systems.animation import AnimatedSprite, Animation

class Collectible(AnimatedSprite):
    """Collectible items that provide benefits to the player"""
    
    def __init__(self, x, y, collectible_type, asset_manager):
        super().__init__(x, y)
        self.collectible_type = collectible_type
        self.asset_manager = asset_manager
        self.collected = False
        self.rect.width = 20
        self.rect.height = 20
        
        # Define animation based on type
        self._setup_animation()
    
    def _setup_animation(self):
        """Set up animations based on collectible type"""
        try:
            # Try to load collectible animation
            if self.collectible_type == "health":
                image = self.asset_manager.load_image("assets/images/collectibles/health.png")
                frames = [image]
            elif self.collectible_type == "coin":
                image = self.asset_manager.load_image("assets/images/collectibles/coin.png")
                frames = [image]
            else:
                # Default collectible
                image = self.asset_manager.create_fallback_image(20, 20)
                frames = [image]
                
            # Create animation
            self.add_animation("idle", Animation(frames, 5))
            self.play_animation("idle")
            
        except Exception as e:
            print(f"Error loading collectible: {e}")
            # Create fallback animation
            fallback = [self.asset_manager.create_fallback_image(20, 20)]
            self.add_animation("idle", Animation(fallback))
            self.play_animation("idle")
    
    def update(self, dt):
        """Update the collectible"""
        # Simple floating animation
        self.update_animation()
    
    def render(self, screen, camera_offset=(0, 0)):
        """Render the collectible with camera offset"""
        if self.collected:
            return
            
        image = self.get_current_frame()
        if image:
            # Apply camera offset if provided
            x = self.rect.x - camera_offset[0]
            y = self.rect.y - camera_offset[1]
            screen.blit(image, (x, y))
