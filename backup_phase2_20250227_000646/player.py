import pygame
from animation import Animation, AnimatedSprite

class Player(AnimatedSprite):
    def __init__(self, x, y, asset_manager):
        super().__init__(x, y)
        
        self.speed = 200
        self.velocity = [0, 0]
        self.is_jumping = False
        self.on_ground = False
        
        # Load player sprites
        idle_frames = asset_manager.load_sprite_sheet("assets/images/player/player_idle.png", 
                                                     50, 50, 8)
        run_frames = asset_manager.load_sprite_sheet("assets/images/player/player_run.png", 
                                                   50, 50, 8)
        jump_frames = asset_manager.load_sprite_sheet("assets/images/player/player_jump.png", 
                                                    50, 50, 4)
        
        # Create animations
        self.add_animation("idle", Animation(idle_frames, 10))
        self.add_animation("run", Animation(run_frames, 8))
        self.add_animation("jump", Animation(jump_frames, 6, loop=False))
        
        # Set default size
        self.rect.width = 50
        self.rect.height = 50
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.on_ground:
                self.is_jumping = True
                self.on_ground = False
                self.velocity[1] = -300
                self.play_animation("jump")
                
    def update(self, dt):
        # Handle movement
        keys = pygame.key.get_pressed()
        self.velocity[0] = 0
        
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
        if not self.on_ground:
            self.velocity[1] += 800 * dt
        
        # Update position
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt
        
        # Simple ground collision
        if self.rect.y > 500:  # Assuming ground is at y=500
            self.rect.y = 500
            self.velocity[1] = 0
            self.on_ground = True
            self.is_jumping = False
            
        # Update animation state
        self.update_animation()
    
    def render(self, screen):
        # Get current sprite frame
        image = self.get_current_frame()
        if image:
            screen.blit(image, self.rect)