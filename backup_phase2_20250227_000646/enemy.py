import pygame
import random
from animation import Animation, AnimatedSprite

class Enemy(AnimatedSprite):
    def __init__(self, x, y, asset_manager):
        super().__init__(x, y)
        self.asset_manager = asset_manager
        
        # Enemy properties
        self.speed = 80
        self.direction = 1  # 1 for right, -1 for left
        self.patrol_distance = 100
        self.start_x = x
        
        # Set default size
        self.rect.width = 50
        self.rect.height = 50
        
        # Load enemy sprite
        self.image = self.asset_manager.load_image("assets/images/enemies/enemy.png")
        
        # Set up simple animation
        frames = [self.image]  # Just using a single frame for simplicity
        self.add_animation("idle", Animation(frames, 10))
        
    def update(self, dt):
        """Update enemy state"""
        # Simple patrol AI
        self.rect.x += self.speed * self.direction * dt
        
        # Change direction when reached patrol limit
        if self.rect.x > self.start_x + self.patrol_distance:
            self.rect.x = self.start_x + self.patrol_distance
            self.direction = -1
            self.facing_right = False
        elif self.rect.x < self.start_x - self.patrol_distance:
            self.rect.x = self.start_x - self.patrol_distance
            self.direction = 1
            self.facing_right = True
            
        # Update animation
        self.update_animation()
    
    def render(self, screen):
        """Render the enemy"""
        # Get current sprite frame
        image = self.get_current_frame() if self.get_current_frame() else self.image
        
        if image:
            screen.blit(image, self.rect)
