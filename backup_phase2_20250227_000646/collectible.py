import pygame
import math

class Collectible:
    def __init__(self, x, y, collectible_type="health", asset_manager=None):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = collectible_type
        self.collected = False
        self.bob_timer = 0
        self.bob_height = 0
        self.bob_direction = 1
        self.bob_speed = 0.1
        self.asset_manager = asset_manager
        
        # Set color based on type
        self.color = self.get_color_by_type()
        
        # Create/load image
        if self.asset_manager:
            # Remove the 'ability_' prefix for the image name
            image_type = collectible_type.replace("ability_", "")
            self.image = self.asset_manager.get_image(f"collectible/{image_type}")
        else:
            # Create a basic image
            self.image = pygame.Surface((20, 20))
            self.image.fill(self.color)
    
    def get_color_by_type(self):
        if self.type == "health":
            return (255, 0, 0)  # Red for health
        elif self.type == "ability_double_jump":
            return (0, 255, 0)  # Green for double jump
        elif self.type == "ability_wall_jump":
            return (0, 0, 255)  # Blue for wall jump
        elif self.type == "ability_dash":
            return (255, 0, 255)  # Purple for dash
        elif self.type == "ability_charged_attack":
            return (255, 255, 0)  # Yellow for charged attack
        else:
            return (255, 255, 255)  # White for default
    
    def update(self):
        # Create bobbing motion
        self.bob_timer += self.bob_speed
        self.bob_height = 3 * math.sin(self.bob_timer)
    
    def render(self, screen, camera_offset):
        if not self.collected:
            if self.image:
                # Draw with bobbing motion
                adjusted_rect = pygame.Rect(
                    self.rect.x - camera_offset[0],
                    self.rect.y - camera_offset[1] + self.bob_height,
                    self.rect.width,
                    self.rect.height
                )
                screen.blit(self.image, adjusted_rect)
            else:
                # Fallback to simple rect
                adjusted_rect = pygame.Rect(
                    self.rect.x - camera_offset[0],
                    self.rect.y - camera_offset[1] + self.bob_height,
                    self.rect.width,
                    self.rect.height
                )
                pygame.draw.rect(screen, self.color, adjusted_rect)
                # Draw outline
                pygame.draw.rect(screen, (255, 255, 255), adjusted_rect, 1)
    
    def collect(self, player):
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            self.apply_effect(player)
            return True
        return False
    
    def apply_effect(self, player):
        if self.type == "health":
            player.heal(25)
        elif self.type.startswith("ability_"):
            ability_name = self.type.replace("ability_", "")
            if ability_name in player.abilities:
                player.abilities[ability_name] = True
                # Special handling for specific abilities
                if ability_name == "double_jump":
                    print("Double jump ability acquired!")
                elif ability_name == "wall_jump":
                    print("Wall jump ability acquired!")
                elif ability_name == "dash":
                    print("Dash ability acquired!")
                elif ability_name == "charged_attack":
                    print("Charged attack ability acquired!")
