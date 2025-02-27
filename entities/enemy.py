import pygame
import math
import random
from systems.animation import AnimatedSprite, Animation

class Enemy(AnimatedSprite):
    """Base class for all enemies"""
    
    def __init__(self, x, y, asset_manager):
        super().__init__(x, y)
        self.asset_manager = asset_manager
        
        # Movement properties
        self.speed = 50
        self.velocity = [0, 0]
        self.direction = 1  # 1 for right, -1 for left
        
        # Stats
        self.health = 100
        self.max_health = 100
        self.damage = 10
        
        # Size
        self.rect.width = 50
        self.rect.height = 50
        
        # Load animations
        self._load_animations()
    
    def _load_animations(self):
        """Load enemy animations"""
        try:
            # Load enemy sprite
            idle_frames = [self.asset_manager.load_image("assets/images/enemies/enemy.png")]
            self.add_animation("idle", Animation(idle_frames, 5))
            self.play_animation("idle")
        except Exception as e:
            print(f"Error loading enemy animations: {e}")
            # Create fallback animation
            fallback = [self.asset_manager.create_fallback_image(50, 50)]
            self.add_animation("idle", Animation(fallback))
            self.play_animation("idle")
    
    def update(self, dt):
        """Update enemy behavior"""
        # Simple movement
        self.velocity[0] = self.speed * self.direction
        
        # Update position
        self.rect.x += self.velocity[0] * dt
        
        # Simple boundary check
        if self.rect.left < 0:
            self.direction = 1
        elif self.rect.right > 2000:  # Assuming level width
            self.direction = -1
        
        # Update animation
        self.update_animation()
    
    def render(self, screen, camera_offset=(0, 0)):
        """Render the enemy with camera offset"""
        image = self.get_current_frame()
        if image:
            # Apply camera offset
            render_x = self.rect.x - camera_offset[0]
            render_y = self.rect.y - camera_offset[1]
            screen.blit(image, (render_x, render_y))
            
            # Draw health bar for enemies
            self._draw_health_bar(screen, camera_offset)
    
    def _draw_health_bar(self, screen, camera_offset):
        """Draw simple health bar above enemy"""
        if self.health < self.max_health:
            bar_width = self.rect.width
            bar_height = 5
            
            # Position above enemy
            x = self.rect.x - camera_offset[0]
            y = self.rect.y - camera_offset[1] - 10
            
            # Background (red)
            pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
            
            # Foreground (green)
            health_width = int((self.health / self.max_health) * bar_width)
            pygame.draw.rect(screen, (0, 255, 0), (x, y, health_width, bar_height))

class Boss(Enemy):
    """Boss enemy with more health and different behavior"""
    def __init__(self, x, y, asset_manager):
        super().__init__(x, y, asset_manager)
        
        # Boss has different stats
        self.health = 500
        self.max_health = 500
        self.damage = 25
        self.speed = 30
        self.rect.width = 100
        self.rect.height = 100
        
        # Override animations
        self._load_animations()
    
    def _load_animations(self):
        """Load boss animations"""
        try:
            # Load boss sprite
            boss_frames = [self.asset_manager.load_image("assets/images/enemies/boss.png")]
            self.add_animation("idle", Animation(boss_frames, 5))
            self.play_animation("idle")
        except Exception as e:
            print(f"Error loading boss animations: {e}")
            # Create fallback animation for boss
            fallback = [self.asset_manager.create_fallback_image(100, 100)]
            self.add_animation("idle", Animation(fallback))
            self.play_animation("idle")
