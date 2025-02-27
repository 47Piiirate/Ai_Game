"""
Script to fix animation and path issues after reorganization
"""
import os

def fix_asset_paths():
    """Create placeholder assets to prevent errors"""
    # Create necessary directories
    directories = [
        "assets/images/player",
        "assets/images/enemies",
        "assets/images/tiles",
        "assets/images/collectibles",
        "assets/images/ui"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create placeholder player images if they don't exist
    player_images = [
        "assets/images/player/player_idle.png",
        "assets/images/player/player_run.png",
        "assets/images/player/player_jump.png"
    ]
    
    import pygame
    pygame.init()
    
    # Create placeholder images for player
    for image_path in player_images:
        if not os.path.exists(image_path):
            print(f"Creating placeholder image: {image_path}")
            # Create a simple placeholder image
            surface = pygame.Surface((400, 50), pygame.SRCALPHA)
            # Draw 8 frames in the spritesheet
            for i in range(8):
                color = (255, 0, 255)  # Magenta
                rect = pygame.Rect(i * 50, 0, 50, 50)
                pygame.draw.rect(surface, color, rect)
                # Draw frame number
                font = pygame.font.Font(None, 24)
                text = font.render(str(i+1), True, (255, 255, 255))
                text_rect = text.get_rect(center=(i * 50 + 25, 25))
                surface.blit(text, text_rect)
            
            # Save the image
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            pygame.image.save(surface, image_path)
    
    # Create placeholder enemy image
    enemy_path = "assets/images/enemies/enemy.png"
    if not os.path.exists(enemy_path):
        print(f"Creating placeholder image: {enemy_path}")
        surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(0, 0, 50, 50))  # Red square
        pygame.draw.line(surface, (0, 0, 0), (0, 0), (50, 50), 2)
        pygame.draw.line(surface, (0, 0, 0), (50, 0), (0, 50), 2)
        os.makedirs(os.path.dirname(enemy_path), exist_ok=True)
        pygame.image.save(surface, enemy_path)
    
    # Create placeholder boss image
    boss_path = "assets/images/enemies/boss.png"
    if not os.path.exists(boss_path):
        print(f"Creating placeholder image: {boss_path}")
        surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(0, 0, 100, 100))  # Red square
        pygame.draw.circle(surface, (0, 0, 0), (50, 50), 40, 2)  # Black circle
        os.makedirs(os.path.dirname(boss_path), exist_ok=True)
        pygame.image.save(surface, boss_path)
    
    pygame.quit()
    
    print("Created placeholder assets to avoid errors")
    return True

if __name__ == "__main__":
    print("Fixing animation paths and creating placeholder assets...")
    fix_asset_paths()
    print("\nScript complete. Try running the game with: python main.py")
