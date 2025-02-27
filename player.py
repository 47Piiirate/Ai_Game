import pygame
from particles import ParticleEffect
from physics_wrapper import sweep_test, check_on_ground

class Player:
    def __init__(self, x, y, level, max_health=100, asset_manager=None):
        # Basic setup
        self.asset_manager = asset_manager
        
        # Load player image if asset manager is available
        if self.asset_manager:
            self.image = self.asset_manager.get_image("player/player")
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Add previous position tracking for wall detection
        self.prev_x = x
        self.prev_y = y
        
        # Movement attributes
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_speed = 5
        self.jump_strength = -12
        self.gravity = 0.5
        self.on_ground = False
        self.facing_right = True
        
        # Dash attributes
        self.can_dash = True
        self.is_dashing = False
        self.dash_time = 0
        self.dash_duration = 15
        self.dash_cooldown = 30
        self.dash_cooldown_timer = 0
        self.dash_speed = 10
        
        # Wall slide attributes
        self.is_wall_sliding = False
        self.wall_slide_speed = 1
        self.wall_jump_strength = -10
        self.touching_wall = False
        
        # Combat attributes
        self.max_health = max_health
        self.health = max_health
        self.stamina = 100
        self.max_stamina = 100
        self.stamina_regen = 0.5
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_damage = 20
        self.attack_rect = pygame.Rect(0, 0, 70, 50)
        self.is_parrying = False
        self.parry_cooldown = 0
        self.parry_window = 10
        self.invulnerable = False
        self.invulnerable_timer = 0
        
        # Ability upgrades
        self.abilities = {
            'double_jump': False,
            'wall_jump': False,
            'dash': True,  # Start with dash ability for testing
            'charged_attack': False
        }
        
        # Level reference
        self.level = level
    
    def update(self, keys, level):
        self.apply_gravity()
        self.handle_movement(keys)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.is_attacking = False
        
        if self.parry_cooldown > 0:
            self.parry_cooldown -= 1
            if self.parry_cooldown <= self.parry_window:
                self.is_parrying = True
            else:
                self.is_parrying = False
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
        
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1
            if self.dash_cooldown_timer <= 0:
                self.can_dash = True
        
        # Handle dash
        if self.is_dashing:
            self.dash_time -= 1
            if self.dash_time <= 0:
                self.is_dashing = False
        
        # Regenerate stamina
        if self.stamina < self.max_stamina:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen)
        
        # Reset flags
        self.on_ground = False
        self.touching_wall = False
        
        # Apply movements and check collisions
        self.check_collisions(level)
        
        # Update attack rect position
        self.update_attack_rect()
    
    def handle_movement(self, keys):
        # Reset horizontal velocity
        self.velocity_x = 0
        
        if self.is_dashing:
            direction = 1 if self.facing_right else -1
            self.velocity_x = self.dash_speed * direction
            return
        
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.max_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.max_speed
            self.facing_right = True
        
        # Jumping
        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.velocity_y = self.jump_strength
            elif self.touching_wall and self.abilities['wall_jump']:
                self.velocity_y = self.jump_strength
                # Push away from wall
                wall_direction = 1 if self.touching_wall == "left" else -1
                self.velocity_x = wall_direction * self.max_speed
        
        # Wall slide
        if self.touching_wall and not self.on_ground and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.is_wall_sliding = True
            if self.velocity_y > self.wall_slide_speed:
                self.velocity_y = self.wall_slide_speed
        else:
            self.is_wall_sliding = False
        
        # Dash
        if keys[pygame.K_c] and self.can_dash and self.abilities['dash'] and self.stamina >= 20:
            self.is_dashing = True
            self.dash_time = self.dash_duration
            self.can_dash = False
            self.dash_cooldown_timer = self.dash_cooldown
            self.stamina -= 20
    
    def apply_gravity(self):
        if not self.on_ground and not self.is_wall_sliding:
            self.velocity_y += self.gravity
            # Terminal velocity
            if self.velocity_y > 10:
                self.velocity_y = 10
    
    def check_collisions(self, level):
        """Check for collisions with level tiles"""
        # Convert tiles to the format expected by our physics functions
        obstacle_rects = []
        for tile in level.tiles:
            obstacle_rects.append((tile.x, tile.y, tile.width, tile.height))
        
        if not obstacle_rects:  # Safeguard against empty levels
            self.on_ground = False
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y
            return
        
        # Use our physics engine for collision detection
        new_x, new_y, collided_x, collided_y = sweep_test(
            self.rect.x, self.rect.y, self.rect.width, self.rect.height,
            self.velocity_x, self.velocity_y, obstacle_rects
        )
        
        # Update position and handle collisions
        self.rect.x = new_x
        self.rect.y = new_y
        
        # Update on_ground flag
        self.on_ground = check_on_ground(
            self.rect.x, self.rect.y, self.rect.width, self.rect.height,
            obstacle_rects
        )
        
        # Handle wall collision (for wall sliding)
        if collided_x:
            self.velocity_x = 0
            if self.rect.x > self.prev_x:
                self.touching_wall = "right"
            elif self.rect.x < self.prev_x:
                self.touching_wall = "left"
        else:
            self.touching_wall = False
        
        # Reset vertical velocity when hitting something above or landing
        if collided_y:
            self.velocity_y = 0
            
        # Store previous position for next frame
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y
    
    def attack(self):
        if self.attack_cooldown <= 0 and self.stamina >= 10:
            self.is_attacking = True
            self.attack_cooldown = 20
            self.stamina -= 10
    
    def parry(self):
        if self.parry_cooldown <= 0 and self.stamina >= 15:
            self.parry_cooldown = 30
            self.stamina -= 15
    
    def dash(self):
        if self.can_dash and self.abilities['dash'] and self.stamina >= 20:
            self.is_dashing = True
            self.dash_time = self.dash_duration
            self.can_dash = False
            self.dash_cooldown_timer = self.dash_cooldown
            self.stamina -= 20
    
    def take_damage(self, amount):
        if not self.invulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable = True
            self.invulnerable_timer = 60  # Invulnerable for 1 second (60 frames)
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    
    def is_alive(self):
        return self.health > 0
    
    def update_attack_rect(self):
        if self.facing_right:
            self.attack_rect.topleft = (self.rect.right, self.rect.y)
        else:
            self.attack_rect.topright = (self.rect.left, self.rect.y)
    
    def create_parry_particles(self):
        particles = []
        for _ in range(10):
            particles.append(ParticleEffect(
                self.rect.centerx, 
                self.rect.centery, 
                (255, 255, 255)
            ))
        return particles
    
    def render(self, screen, camera_offset):
        # Draw player
        player_rect = self.rect.copy()
        player_rect.x -= camera_offset[0]
        player_rect.y -= camera_offset[1]
        
        # Flash when invulnerable
        if self.invulnerable and self.invulnerable_timer % 6 < 3:
            screen.blit(self.image, player_rect.topleft)
        elif not self.invulnerable:
            screen.blit(self.image, player_rect.topleft)
        
        # Draw attack hitbox if attacking
        if self.is_attacking:
            attack_rect = self.attack_rect.copy()
            attack_rect.x -= camera_offset[0]
            attack_rect.y -= camera_offset[1]
            pygame.draw.rect(screen, (255, 0, 0, 128), attack_rect, 1)
        
        # Draw parry effect if parrying
        if self.is_parrying:
            parry_rect = pygame.Rect(0, 0, 70, 70)
            parry_rect.center = player_rect.center
            pygame.draw.circle(screen, (0, 255, 255, 128), parry_rect.center, 35, 2)