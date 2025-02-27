import pygame
import math

class Projectile:
    def __init__(self, x, y, direction, speed=8, damage=10, owner="player", lifetime=180):
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 255, 0) if owner == "player" else (0, 0, 255))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Convert direction to radians if it's in degrees
        if isinstance(direction, (int, float)):
            self.direction_rad = math.radians(direction)
        else:
            # If direction is already a normalized vector
            self.direction_rad = math.atan2(direction[1], direction[0])
            
        self.speed = speed
        self.damage = damage
        self.owner = owner  # "player" or "enemy"
        self.lifetime = lifetime
        
        # Calculate velocity
        self.velocity_x = math.cos(self.direction_rad) * speed
        self.velocity_y = math.sin(self.direction_rad) * speed
    
    def update(self):
        # Move projectile
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Reduce lifetime
        self.lifetime -= 1
    
    def render(self, screen, camera_offset):
        # Apply camera offset
        proj_rect = self.rect.copy()
        proj_rect.x -= camera_offset[0]
        proj_rect.y -= camera_offset[1]
        
        # Rotate image to match direction
        angle = math.degrees(self.direction_rad)
        rotated_image = pygame.transform.rotate(self.image, -angle)
        rotated_rect = rotated_image.get_rect(center=proj_rect.center)
        
        # Draw projectile
        screen.blit(rotated_image, rotated_rect.topleft)
    
    def is_expired(self):
        return self.lifetime <= 0

class ChargedProjectile(Projectile):
    def __init__(self, x, y, direction, charge_level=1.0, **kwargs):
        super().__init__(x, y, direction, **kwargs)
        
        # Scale damage and size based on charge level
        self.damage *= charge_level
        
        # Create a larger projectile based on charge level
        size = int(10 * charge_level)
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 0) if self.owner == "player" else (0, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))
