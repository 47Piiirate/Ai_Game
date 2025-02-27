import pygame
from systems.animation import Animation, AnimatedSprite

class Player(AnimatedSprite):
    """Player character with movement, collision, and abilities"""
    
    def __init__(self, x, y, asset_manager):
        super().__init__(x, y)
        self.asset_manager = asset_manager
        
        # Movement properties
        self.velocity = [0, 0]
        self.speed = 200
        self.jump_power = 500
        self.gravity = 800
        self.on_ground = False
        self.is_jumping = False
        self.facing_right = True
        
        # Combat properties
        self.health = 100
        self.max_health = 100
        self.coins = 0
        self.damage = 10
        self.attack_cooldown = 0
        self.invincibility_frames = 0
        
        # Size
        self.rect.width = 50
        self.rect.height = 50
        
        # Load animations
        self._load_animations()
    
    def _load_animations(self):
        """Load player animations from sprite sheets"""
        try:
            # Load animation frames from sprite sheets
            idle_frames = self.asset_manager.load_sprite_sheet(
                "assets/images/player/player_idle.png", 50, 50, 8)
            run_frames = self.asset_manager.load_sprite_sheet(
                "assets/images/player/player_run.png", 50, 50, 8)
            jump_frames = self.asset_manager.load_sprite_sheet(
                "assets/images/player/player_jump.png", 50, 50, 4)
            
            # Create animations with appropriate durations
            self.add_animation("idle", Animation(idle_frames, 10))
            self.add_animation("run", Animation(run_frames, 6))
            self.add_animation("jump", Animation(jump_frames, 5, loop=False))
            
            # Set initial animation
            self.play_animation("idle")
            
        except Exception as e:
            print(f"Error loading player animations: {e}")
            # Create fallback animations if loading fails
            fallback = [self.asset_manager.create_fallback_image(50, 50)]
            self.add_animation("idle", Animation(fallback))
            self.add_animation("run", Animation(fallback))
            self.add_animation("jump", Animation(fallback))
    
    def handle_event(self, event):
        """Handle player input events"""
        if event.type == pygame.KEYDOWN:
            # Jump when space is pressed
            if event.key == pygame.K_SPACE and self.on_ground:
                self.velocity[1] = -self.jump_power
                self.on_ground = False
                self.is_jumping = True
                self.play_animation("jump")
            # Attack
            elif event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                self.attack()
    
    def update(self, dt):
        """Update player state and position"""
        # Handle cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        if self.invincibility_frames > 0:
            self.invincibility_frames -= dt
        
        # Get keyboard state for movement
        keys = pygame.key.get_pressed()
        
        # Reset horizontal velocity
        self.velocity[0] = 0
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity[0] = -self.speed
            self.facing_right = False
            if self.on_ground and not self.is_jumping:
                self.play_animation("run")
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity[0] = self.speed
            self.facing_right = True
            if self.on_ground and not self.is_jumping:
                self.play_animation("run")
        else:
            if self.on_ground and not self.is_jumping:
                self.play_animation("idle")
        
        # Apply gravity
        self.velocity[1] += self.gravity * dt
        
        # Update position
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt
        
        # Ensure player can't go off screen horizontally
        self.rect.x = max(0, min(self.rect.x, 2000 - self.rect.width))
        
        # Check if player is on ground (basic check)
        # This will be replaced by platform collision in the Game class
        if self.rect.y > 500:  # Ground level
            self.rect.y = 500
            self.velocity[1] = 0
            self.on_ground = True
            
            if self.is_jumping:
                self.is_jumping = False
                # Return to idle or run animation
                if abs(self.velocity[0]) > 0:
                    self.play_animation("run")
                else:
                    self.play_animation("idle")
        
        # Update animation
        self.update_animation()
    
    def attack(self):
        """Initiate an attack"""
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 0.5  # Half second cooldown
            # Attack logic would go here (create projectile, check hit, etc)
            print("Player attacks!")
    
    def take_damage(self, amount):
        """Take damage and handle invincibility frames"""
        if self.invincibility_frames <= 0:
            self.health -= amount
            self.invincibility_frames = 1.0  # 1 second of invincibility
            
            if self.health <= 0:
                self.die()
    
    def die(self):
        """Handle player death"""
        print("Player died!")
        # Death logic would go here
    
    def render(self, screen, camera_offset=(0, 0)):
        """Render the player with camera offset"""
        # Get current animation frame
        image = self.get_current_frame()
        
        if image:
            # Apply camera offset for rendering
            render_x = self.rect.x - camera_offset[0]
            render_y = self.rect.y - camera_offset[1]
            
            # Flashing effect during invincibility
            if self.invincibility_frames > 0 and int(pygame.time.get_ticks() / 100) % 2 == 0:
                # Skip rendering every other frame to create flashing effect
                pass
            else:
                screen.blit(image, (render_x, render_y))