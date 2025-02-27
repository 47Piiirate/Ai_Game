import pygame
from enemy import Enemy, Boss
import random
import room
import item
from collectible import Collectible
from player import Player
from asset_manager import AssetManager
from level import Level

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.assets = AssetManager()
        self.level = Level(self.assets)
        self.player = Player(400, 300, self.assets)
        self.running = True
        self.camera = None
        self.ui = None
        self.sound_manager = None
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.current_level_name = "starting_area"
        self.game_state = "playing"  # playing, paused, game_over, level_transition
        self.transition_timer = 0
        
        # Initialize basic game elements
        self._initialize_game_elements()
    
    def _initialize_game_elements(self):
        """Initialize basic game elements like enemies and collectibles"""
        # Add some enemies
        self.enemies = [
            Enemy(200, 300, self.assets),
            Enemy(600, 300, self.assets)
        ]
        
        # Add some collectibles
        self.collectibles = [
            Collectible(300, 400, "health", self.assets),
            Collectible(500, 400, "coin", self.assets)
        ]
    
    def handle_event(self, event):
        """Handle game events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
        
        # Let player handle events
        self.player.handle_event(event)
    
    def update(self, dt):
        """Update game state"""
        # Update player and check level collisions
        self.player.update(dt, self.level)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(dt)
            
        # Update collectibles and check collisions
        for collectible in self.collectibles[:]:
            collectible.update(dt)
            if collectible.rect.colliderect(self.player.rect):
                # Player collected this item
                self.collectibles.remove(collectible)
    
    def render(self, screen):
        """Render game elements"""
        # Draw level (background and platforms)
        self.level.render(screen)
        
        # Draw collectibles
        for collectible in self.collectibles:
            collectible.render(screen)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.render(screen)
            
        # Draw player
        self.player.render(screen)
        
        # Apply camera offset to everything we render
        camera_offset = self.camera.get_offset()
        
        # Render the level
        self.level.render(screen, camera_offset)
        
        # Render enemies
        for enemy in self.enemies:
            enemy.render(screen, camera_offset)
        
        # Render collectibles
        for collectible in self.collectibles:
            collectible.render(screen, camera_offset)
        
        # Render player
        self.player.render(screen, camera_offset)
        
        # Render projectiles
        for projectile in self.projectiles:
            projectile.render(screen, camera_offset)
        
        # Render particles
        for particle in self.particles:
            particle.render(screen, camera_offset)
        
        # Render UI (no camera offset for UI)
        self.ui.render(screen, self.player)
        
        # Render level transition effect
        if self.game_state == "level_transition":
            # Create fade effect
            overlay = pygame.Surface((screen.get_width(), screen.get_height()))
            alpha = min(255, (self.transition_timer / 30) * 255)
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Display level name
            if self.transition_timer < 15:  # Show name in second half of transition
                font = pygame.font.Font(None, 36)
                level_text = font.render(f"Entering: {self.current_level_name.replace('_', ' ').title()}", 
                                      True, (255, 255, 255))
                text_rect = level_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
                screen.blit(level_text, text_rect)
        
        # Render pause or game over screen
        if self.game_state == "paused":
            self.render_pause_screen(screen)
        elif self.game_state == "game_over":
            self.render_game_over_screen(screen)
    
    def render_pause_screen(self, screen):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
    
    def render_game_over_screen(self, screen):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(192)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
