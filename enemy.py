import pygame
import random
from particles import ParticleEffect

class Enemy:
    def __init__(self, x, y, max_health=50, asset_manager=None):
        # Basic setup
        self.asset_manager = asset_manager
        
        # Load enemy image if asset manager is available
        if self.asset_manager:
            self.image = self.asset_manager.get_image("enemy/enemy")
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 0, 255))
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Movement attributes
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 2
        self.gravity = 0.5
        self.direction = 1  # 1 for right, -1 for left
        self.movement_timer = 0
        self.jump_timer = 0
        self.on_ground = False
        
        # Combat attributes
        self.max_health = max_health
        self.health = max_health
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_damage = 10
        self.attack_rect = pygame.Rect(0, 0, 60, 40)
        self.aggro_range = 300
        self.attack_range = 70
        
        # State
        self.state = "patrol"  # patrol, chase, attack, idle
        self.patrol_point_a = x - 100
        self.patrol_point_b = x + 100
    
    def update(self, player):
        # Apply gravity
        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10
        
        # Basic AI state machine
        dist_to_player = abs(self.rect.centerx - player.rect.centerx)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.is_attacking = False
        
        # Update state based on player distance
        if dist_to_player < self.attack_range and abs(self.rect.centery - player.rect.centery) < 50:
            self.state = "attack"
        elif dist_to_player < self.aggro_range:
            self.state = "chase"
        else:
            self.state = "patrol"
        
        # Execute behavior based on state
        if self.state == "patrol":
            self.patrol()
        elif self.state == "chase":
            self.chase(player)
        elif self.state == "attack":
            self.attack(player)
        
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Check if on ground
        if self.rect.bottom >= 600:  # Assuming ground level is at y = 600
            self.rect.bottom = 600
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
    
    def patrol(self):
        if self.movement_timer <= 0:
            self.direction *= -1
            self.movement_timer = random.randint(60, 120)
        self.velocity_x = self.speed * self.direction
        self.movement_timer -= 1
    
    def chase(self, player):
        if self.rect.x < player.rect.x:
            self.velocity_x = self.speed
        elif self.rect.x > player.rect.x:
            self.velocity_x = -self.speed
        if self.rect.y < player.rect.y:
            self.velocity_y = self.speed
        elif self.rect.y > player.rect.y:
            self.velocity_y = -self.speed
    
    def attack(self, player):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_cooldown = 60  # Cooldown period for next attack
            if self.attack_rect.colliderect(player.rect):
                player.take_damage(self.attack_damage)
    
    def render(self, screen, camera_offset):
        # Apply camera offset
        enemy_rect = self.rect.copy()
        enemy_rect.x -= camera_offset[0]
        enemy_rect.y -= camera_offset[1]
        screen.blit(self.image, enemy_rect.topleft)
        self.render_health_bar(screen, camera_offset)

    def render_health_bar(self, screen, camera_offset):
        health_bar_width = 50
        health_bar_height = 5
        fill = (self.health / self.max_health) * health_bar_width
        
        # Apply camera offset to health bar
        outline_rect = pygame.Rect(
            self.rect.x - camera_offset[0], 
            self.rect.y - 10 - camera_offset[1], 
            health_bar_width, 
            health_bar_height
        )
        fill_rect = pygame.Rect(
            self.rect.x - camera_offset[0], 
            self.rect.y - 10 - camera_offset[1], 
            fill, 
            health_bar_height
        )
        
        pygame.draw.rect(screen, (0, 0, 255), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 1)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.die()

    def die(self):
        # Placeholder for death logic
        pass


class Boss(Enemy):
    def __init__(self, x, y, max_health=200, asset_manager=None):
        super().__init__(x, y, max_health, asset_manager)
        
        # Override base enemy properties
        if self.asset_manager:
            self.image = self.asset_manager.get_image("enemy/boss")
        else:
            self.image = pygame.Surface((100, 100))
            self.image.fill((255, 0, 100))
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Boss-specific attributes
        self.attack_damage = 25
        self.speed = 1.5
        self.attack_cooldown = 0
        self.attack_range = 120
        self.aggro_range = 500
        self.phase = 1  # Boss can have multiple phases
        self.attack_pattern = 0  # Current attack pattern
        self.attack_timer = 0
        self.charge_speed = 8
        
        # Attack rect for different attacks
        self.attack_rect = pygame.Rect(0, 0, 120, 80)
    
    def update(self, player):
        # Apply gravity similar to base enemy
        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10
            
        # Always chase the player when in range
        dist_to_player = abs(self.rect.centerx - player.rect.centerx)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.is_attacking = False
        
        # Boss is always aware of player
        if dist_to_player < self.attack_range and abs(self.rect.centery - player.rect.centery) < 70:
            self.state = "attack"
        else:
            self.state = "chase"
        
        # Phase transition based on health
        if self.health < self.max_health * 0.5 and self.phase == 1:
            self.phase = 2
            self.speed += 1
            self.attack_damage += 10
        
        # Execute behavior based on state
        if self.state == "chase":
            self.chase(player)
        elif self.state == "attack":
            self.execute_attack_pattern(player)
        
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Check if on ground (simplified)
        if self.rect.bottom >= 600:  
            self.rect.bottom = 600
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        # Update attack rect position
        self.update_attack_rect()
    
    def execute_attack_pattern(self, player):
        # Different attack patterns based on phase and timer
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_cooldown = 90  # Longer cooldown for boss
            
            # Choose attack pattern
            self.attack_pattern = random.randint(0, 2)
            
            if self.attack_pattern == 0:
                # Basic attack
                if self.attack_rect.colliderect(player.rect):
                    player.take_damage(self.attack_damage)
            
            elif self.attack_pattern == 1:
                # Charge attack
                direction = 1 if self.rect.x < player.rect.x else -1
                self.velocity_x = self.charge_speed * direction
            
            elif self.attack_pattern == 2:
                # Jump attack (if on ground)
                if self.on_ground:
                    self.velocity_y = -15  # Jump higher than player
    
    def update_attack_rect(self):
        # Update the attack hitbox location
        self.attack_rect.center = self.rect.center
        
    def render(self, screen, camera_offset):
        # Apply camera offset
        boss_rect = self.rect.copy()
        boss_rect.x -= camera_offset[0]
        boss_rect.y -= camera_offset[1]
        screen.blit(self.image, boss_rect.topleft)
        
        # Draw larger health bar for boss
        self.render_boss_health_bar(screen, camera_offset)
        
        # Draw attack rect for debugging
        if self.is_attacking:
            attack_rect = self.attack_rect.copy()
            attack_rect.x -= camera_offset[0]
            attack_rect.y -= camera_offset[1]
            pygame.draw.rect(screen, (255, 0, 0, 128), attack_rect, 2)
    
    def render_boss_health_bar(self, screen, camera_offset):
        health_bar_width = 150
        health_bar_height = 10
        fill = (self.health / self.max_health) * health_bar_width
        
        # Position at top of screen regardless of camera
        outline_rect = pygame.Rect(
            (screen.get_width() - health_bar_width) // 2,
            30,
            health_bar_width,
            health_bar_height
        )
        fill_rect = pygame.Rect(
            (screen.get_width() - health_bar_width) // 2,
            30,
            fill,
            health_bar_height
        )
        
        pygame.draw.rect(screen, (255, 0, 100), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)
        
        # Draw boss name
        font = pygame.font.Font(None, 24)
        text = font.render("BOSS", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, 20))
        screen.blit(text, text_rect)
