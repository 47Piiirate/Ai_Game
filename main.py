"""
AI Game - Main Entry Point
Initializes the game environment and starts the game
"""
import pygame
import sys
import os

# Set up environment
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"  # Hide pygame welcome message

def setup_environment():
    """Setup the game environment before launch"""
    # Create necessary asset directories if they don't exist
    directories = [
        "assets/images/player",
        "assets/images/enemies",
        "assets/images/collectibles",
        "assets/images/tiles",
        "assets/images/ui",
        "saves"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create placeholder assets if they don't exist
    create_placeholder_assets()

def create_placeholder_assets():
    """Create placeholder assets for testing"""
    # Define assets that need to be created
    assets = {
        "player": [
            "assets/images/player/player_idle.png",
            "assets/images/player/player_run.png",
            "assets/images/player/player_jump.png"
        ],
        "enemies": [
            "assets/images/enemies/enemy.png",
            "assets/images/enemies/boss.png"
        ],
        "collectibles": [
            "assets/images/collectibles/health.png",
            "assets/images/collectibles/coin.png"
        ],
        "tiles": [
            "assets/images/tiles/background.png"
        ]
    }
    
    # Initialize pygame for surface creation
    pygame.init()
    
    # Create player animations
    create_player_assets(assets["player"])
    
    # Create enemy images
    create_enemy_assets(assets["enemies"])
    
    # Create collectible images
    create_collectible_assets(assets["collectibles"])
    
    # Create tile images
    create_tile_assets(assets["tiles"])
    
    print("Asset creation complete")

def create_player_assets(assets):
    """Create player animation placeholder images"""
    colors = {
        "idle": (0, 255, 0),    # Green
        "run": (0, 0, 255),     # Blue
        "jump": (255, 255, 0)   # Yellow
    }
    
    for path in assets:
        if not os.path.exists(path):
            print(f"Creating {path}")
            
            # Determine type from filename
            asset_type = path.split('_')[-1].split('.')[0]
            color = colors.get(asset_type, (255, 0, 255))  # Default to magenta
            
            # Create spritesheet with 8 frames (or 4 for jump)
            frames = 4 if "jump" in path else 8
            width = 50 * frames
            height = 50
            
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Create frames
            for i in range(frames):
                rect = pygame.Rect(i * 50, 0, 50, 50)
                pygame.draw.rect(surface, color, rect)
                # Add frame number
                font = pygame.font.Font(None, 24)
                text = font.render(str(i+1), True, (255, 255, 255))
                text_rect = text.get_rect(center=(i * 50 + 25, 25))
                surface.blit(text, text_rect)
                
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pygame.image.save(surface, path)

def create_enemy_assets(assets):
    """Create enemy placeholder images"""
    for path in assets:
        if not os.path.exists(path):
            print(f"Creating {path}")
            surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(0, 0, 100, 100))
            pygame.draw.circle(surface, (0, 0, 0), (50, 50), 40, 2)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pygame.image.save(surface, path)

def create_collectible_assets(assets):
    """Create collectible placeholder images"""
    for path in assets:
        if not os.path.exists(path):
            print(f"Creating {path}")
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 255, 0), (25, 25), 20)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pygame.image.save(surface, path)

def create_tile_assets(assets):
    """Create tile placeholder images"""
    for path in assets:
        if not os.path.exists(path):
            print(f"Creating {path}")
            surface = pygame.Surface((800, 600), pygame.SRCALPHA)
            pygame.draw.rect(surface, (0, 255, 255), pygame.Rect(0, 0, 800, 600))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pygame.image.save(surface, path)

def main():
    """Main function to start the game"""
    setup_environment()
    
    try:
        # Initialize pygame first
        pygame.init()
        
        # Then import our game modules
        from core.app import App
        from utils.logger import setup_logger
        
        # Set up logging
        setup_logger(log_to_file=True)  # Pass log_to_file parameter
        
        # Create and run application
        app = App()
        app.run()
        
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
