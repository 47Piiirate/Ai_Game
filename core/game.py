"""
Core game logic and state management
"""
import pygame
import logging
from entities.player import Player
from entities.enemy import Enemy
from entities.collectible import Collectible
from utils.asset_manager import AssetManager
from core.level import Level

logger = logging.getLogger(__name__)

class Game:
    """
    Main game class that manages game logic and state
    """
    def __init__(self, screen, controller=None, camera=None, ui=None, config=None):
        """
        Initialize the game
        
        Args:
            screen: Pygame surface for rendering
            controller: Controller for input handling
            camera: Camera for screen scrolling
            ui: UI renderer
            config: Game configuration
        """
        self.screen = screen
        self.controller = controller
        self.camera = camera
        self.ui = ui
        self.config = config
        
        # Initialize asset manager
        self.assets = AssetManager()
        
        # Game state
        self.running = True
        self.game_state = "playing"  # playing, paused, game_over, level_completed
        
        # Initialize level
        self.level = Level(self.assets)
        
        # Initialize player
        screen_width, screen_height = screen.get_size()
        player_x = screen_width // 2
        player_y = screen_height // 2
        self.player = Player(player_x, player_y, self.assets)
        
        # Game objects
        self.enemies = []
        self.collectibles = []
        self.projectiles = []
        
        # Set up initial game elements
        self._initialize_game_elements()
        
        logger.info("Game initialized")
    
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
        
        logger.info("Game elements initialized")
    
    def handle_event(self, event):
        """Handle game events"""
        if event.type == pygame.KEYDOWN:
            # Handle key presses
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            elif event.key == pygame.K_r and self.game_state == "game_over":
                self.restart()
        
        # Let player handle events if game is running
        if self.game_state == "playing" and hasattr(self.player, 'handle_event'):
            self.player.handle_event(event)
    
    def toggle_pause(self):
        """Toggle between playing and paused states"""
        if self.game_state == "playing":
            self.game_state = "paused"
            logger.info("Game paused")
        elif self.game_state == "paused":
            self.game_state = "playing"
            logger.info("Game resumed")
    
    def restart(self):
        """Restart the game"""
        self.game_state = "playing"
        
        # Reset player
        screen_width, screen_height = self.screen.get_size()
        self.player = Player(screen_width // 2, screen_height // 2, self.assets)
        
        # Reset game elements
        self._initialize_game_elements()
        
        logger.info("Game restarted")
    
    def update(self, dt):
        """Update game state"""
        # Only update if the game is playing
        if self.game_state != "playing":
            return
        
        # Update player
        if hasattr(self.player, 'update'):
            self.player.update(dt)
        
        # Handle player-level collision
        if hasattr(self.level, 'check_collision'):
            # Check player feet for ground collision
            feet_rect = pygame.Rect(
                self.player.rect.x,
                self.player.rect.y + self.player.rect.height - 5,
                self.player.rect.width,
                5
            )
            
            ground_collisions = self.level.check_collision(feet_rect)
            if ground_collisions:
                # Set player on ground
                self.player.rect.bottom = ground_collisions[0].top
                self.player.velocity[1] = 0
                self.player.on_ground = True
        
        # Update enemies
        for enemy in self.enemies:
            if hasattr(enemy, 'update'):
                enemy.update(dt)
        
        # Update collectibles and check player collection
        for collectible in self.collectibles[:]:
            if hasattr(collectible, 'update'):
                collectible.update(dt)
            
            if collectible.rect.colliderect(self.player.rect):
                if collectible.collectible_type == "health":
                    # Health pickup
                    self.player.health = min(self.player.health + 25, self.player.max_health)
                elif collectible.collectible_type == "coin":
                    # Coin pickup
                    if not hasattr(self.player, 'coins'):
                        self.player.coins = 0
                    self.player.coins += 1
                
                self.collectibles.remove(collectible)
                logger.debug(f"Collected {collectible.collectible_type}")
        
        # Update camera to follow player
        if self.camera:
            self.camera.follow(self.player)
    
    def render(self, screen):
        """Render the game"""
        # Get camera offset if camera exists
        camera_offset = self.camera.get_offset() if self.camera else (0, 0)
        
        # Draw level
        if hasattr(self.level, 'render'):
            self.level.render(screen, camera_offset)
        
        # Draw collectibles
        for collectible in self.collectibles:
            collectible.render(screen, camera_offset)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.render(screen, camera_offset)
            
        # Draw player
        self.player.render(screen, camera_offset)
        
        # Draw UI (if exists)
        if self.ui:
            self.ui.render(screen, self.player)
        
        # Render game state overlays
        if self.game_state == "paused":
            self._render_pause_screen(screen)
        elif self.game_state == "game_over":
            self._render_game_over_screen(screen)
    
    def _render_pause_screen(self, screen):
        """Render the pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Pause text
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        
        # Instructions
        font_small = pygame.font.Font(None, 30)
        instruct = font_small.render("Press ESC to resume", True, (200, 200, 200))
        instruct_rect = instruct.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        screen.blit(instruct, instruct_rect)
    
    def _render_game_over_screen(self, screen):
        """Render the game over screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(192)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        
        # Instructions
        font_small = pygame.font.Font(None, 30)
        instruct = font_small.render("Press R to restart", True, (200, 200, 200))
        instruct_rect = instruct.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        screen.blit(instruct, instruct_rect)
