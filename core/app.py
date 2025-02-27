"""
Main application class that manages the game loop
"""
import pygame
import sys
import logging

from core.game import Game
from core.config import Config
from systems.camera import Camera
from graphics.ui import UI
from systems.controller import Controller

logger = logging.getLogger(__name__)

class App:
    """
    Main application class
    """
    def __init__(self):
        """Initialize the application"""
        # Load configuration
        self.config = Config()
        
        # Initialize display
        self.width = self.config.get("video", "width", 800)
        self.height = self.config.get("video", "height", 600)
        self.fullscreen = self.config.get("video", "fullscreen", False)
        self.vsync = self.config.get("video", "vsync", True)
        
        # Initialize pygame
        pygame.init()
        
        # Set up the display
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if self.fullscreen:
            flags |= pygame.FULLSCREEN
        
        if self.vsync:
            self.screen = pygame.display.set_mode((self.width, self.height), flags, vsync=1)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), flags)
            
        pygame.display.set_caption("AI Game")
        
        # Set up game components
        self.clock = pygame.time.Clock()
        self.fps_limit = self.config.get("video", "fps_limit", 60)
        self.controller = Controller()
        self.camera = Camera(self.width, self.height)
        self.ui = UI(self.width, self.height)
        
        # Initialize game
        self.game = Game(self.screen, self.controller, self.camera, self.ui, self.config)
        
        # Game state
        self.running = True
        
        logger.info("Application initialized")
    
    def run(self):
        """Run the game loop"""
        logger.info("Starting game loop")
        
        try:
            while self.running:
                # Calculate delta time
                dt = self.clock.tick(self.fps_limit) / 1000.0
                
                # Process events
                self._process_events()
                
                # Update controller
                self.controller.update()
                
                # Update game
                self.game.update(dt)
                
                # Render
                self.screen.fill((0, 0, 0))  # Clear screen
                self.game.render(self.screen)
                
                # Display FPS if configured
                if self.config.get("gameplay", "show_fps", False):
                    self._show_fps()
                
                # Flip the display
                pygame.display.flip()
                
        except Exception as e:
            logger.error(f"Error in game loop: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        finally:
            self.quit()
    
    def _process_events(self):
        """Process events from the event queue"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                # Toggle fullscreen with F11
                self._toggle_fullscreen()
            
            # Pass events to game
            self.game.handle_event(event)
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen
        
        # Update config
        self.config.set("video", "fullscreen", self.fullscreen)
        self.config.save()
        
        # Change display mode
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if self.fullscreen:
            flags |= pygame.FULLSCREEN
        
        if self.vsync:
            self.screen = pygame.display.set_mode((self.width, self.height), flags, vsync=1)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), flags)
            
        logger.info(f"Fullscreen toggled: {self.fullscreen}")
    
    def _show_fps(self):
        """Display FPS counter"""
        fps = int(self.clock.get_fps())
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
    
    def quit(self):
        """Clean up and quit"""
        logger.info("Shutting down")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()
