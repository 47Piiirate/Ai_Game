import pygame
import sys
from game import Game
from camera import Camera

class App:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up display
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI Game")
        
        # Set up game objects
        self.clock = pygame.time.Clock()
        self.game = Game(self.screen)
        self.camera = Camera(self.width, self.height)
        
    def run(self):
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.game.handle_event(event)
            
            # Update
            dt = self.clock.tick(60) / 1000.0
            self.game.update(dt)
            
            # Update camera to follow player
            self.camera.follow(self.game.player)
            
            # Render
            self.screen.fill((0, 0, 0))
            self.game.render(self.screen)
            pygame.display.flip()
    
    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()
