import pygame
import sys
import os

# Add proper error handling for imports
try:
    from game import Game
    from camera import Camera
    from player import Player
    from level import Level
    from ui import UI
    from game_state import GameState
    from sound_manager import SoundManager
    from asset_manager import AssetManager  # New import
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required files are in the correct location.")
    sys.exit(1)

# Make sure assets directory exists
try:
    os.makedirs("assets/sounds", exist_ok=True)
    os.makedirs("assets/music", exist_ok=True)
    os.makedirs("assets/images", exist_ok=True)
except Exception as e:
    print(f"Error creating asset directories: {e}")

def main():
    # Initialize pygame with error handling
    try:
        pygame.init()
        print("Pygame initialized successfully")
        print("Using pure Python physics implementation")
    except Exception as e:
        print(f"Error initializing pygame: {e}")
        return
    
    # Print diagnostic info
    print(f"Pygame version: {pygame.version.ver}")
    print(f"SDL version: {'.'.join(str(v) for v in pygame.version.SDL)}")
    
    # Set up the display
    try:
        screen_width = 1280
        screen_height = 720
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Metroidvania Game")
        print("Display initialized successfully")
    except Exception as e:
        print(f"Error setting up display: {e}")
        return
    
    # Create game clock
    clock = pygame.time.Clock()
    FPS = 60
    
    # Create asset manager first so it's available to other objects
    asset_manager = AssetManager()
    print("Asset manager initialized")
    
    # Create game objects with error handling
    try:
        game_state = GameState()
        sound_manager = SoundManager()
        level = Level(asset_manager=asset_manager)  # Pass asset manager
        player = Player(100, 100, level, asset_manager=asset_manager)  # Pass asset manager
        camera = Camera(screen_width, screen_height)
        ui = UI()
        game = Game(level, player, camera, ui, sound_manager, asset_manager=asset_manager)  # Pass asset manager
        print("Game objects created successfully")
    except Exception as e:
        print(f"Error creating game objects: {e}")
        return
    
    # Enable key repeat (helps with smooth menu navigation)
    pygame.key.set_repeat(200, 100)
    
    print("Starting game loop...")
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state.state == "menu":
                game_state.handle_menu_input(event)
                # Play menu selection sound
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    try:
                        sound_manager.play_sound("menu_select")
                    except:
                        pass  # Ignore sound errors
            elif game_state.state == "playing":
                game.handle_event(event)
                
                # Check for pause key (Escape)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state.state = "paused"
                    try:
                        sound_manager.play_sound("menu_select")
                        sound_manager.pause_music()
                    except:
                        pass  # Ignore sound errors
            elif game_state.state == "paused":
                # Resume game if escape is pressed again
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state.state = "playing"
                    try:
                        sound_manager.play_sound("menu_select")
                        sound_manager.unpause_music()
                    except:
                        pass  # Ignore sound errors
                    
                # Save game when S is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    game_state.save_game(player, level, game.enemies)
                    try:
                        sound_manager.play_sound("menu_select")
                    except:
                        pass  # Ignore sound errors
                    
                # Return to menu when M is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    game_state.state = "menu"
                    try:
                        sound_manager.play_sound("menu_select")
                        sound_manager.play_music("title")
                    except:
                        pass  # Ignore sound errors
        
        # Update game state
        try:
            keys = pygame.key.get_pressed()
            if game_state.state == "playing":
                game.update(keys)
                
                # Check if player died
                if game.game_state == "game_over":
                    game_state.state = "game_over"
                    try:
                        sound_manager.play_music("game_over", False)
                    except:
                        pass  # Ignore sound errors
        except Exception as e:
            print(f"Error in update loop: {e}")
        
        # Try to play appropriate music for current state
        try:
            if game_state.state == "menu" and sound_manager.current_music != "title":
                sound_manager.play_music("title")
            elif game_state.state == "playing" and game.current_level_name == "starting_area" and sound_manager.current_music != "main_area":
                sound_manager.play_music("main_area")
            elif game_state.state == "playing" and game.current_level_name == "underground_cave" and sound_manager.current_music != "cave":
                sound_manager.play_music("cave")
            elif game_state.state == "playing" and game.current_level_name == "boss_chamber" and sound_manager.current_music != "boss":
                sound_manager.play_music("boss")
        except Exception as e:
            print(f"Error playing music: {e}")  # Just log the error and continue
            
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Render based on current state
        try:
            if game_state.state == "menu":
                game_state.render_menu(screen)
            elif game_state.state in ["playing", "paused"]:
                game.render(screen)
                
                # Show pause overlay
                if game_state.state == "paused":
                    # Semi-transparent overlay
                    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 128))
                    screen.blit(overlay, (0, 0))
                    
                    # Pause text
                    font = pygame.font.Font(None, 74)
                    text = font.render("PAUSED", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
                    screen.blit(text, text_rect)
                    
                    # Instructions
                    font_small = pygame.font.Font(None, 36)
                    text1 = font_small.render("Press ESC to resume", True, (255, 255, 255))
                    text2 = font_small.render("Press S to save game", True, (255, 255, 255))
                    text3 = font_small.render("Press M to return to menu", True, (255, 255, 255))
                    screen.blit(text1, (screen_width // 2 - text1.get_width() // 2, screen_height // 2 + 10))
                    screen.blit(text2, (screen_width // 2 - text2.get_width() // 2, screen_height // 2 + 50))
                    screen.blit(text3, (screen_width // 2 - text3.get_width() // 2, screen_height // 2 + 90))
            
            # Game over screen
            elif game_state.state == "game_over":
                # Background
                screen.fill((0, 0, 0))
                
                # Game over text
                font_title = pygame.font.Font(None, 100)
                text = font_title.render("GAME OVER", True, (255, 0, 0))
                text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
                screen.blit(text, text_rect)
                
                # Press any key text
                font_small = pygame.font.Font(None, 36)
                if pygame.time.get_ticks() % 1000 < 500:  # Blinking text
                    text = font_small.render("Press any key to continue", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
                    screen.blit(text, text_rect)
                    
        except Exception as e:
            print(f"Error in rendering: {e}")
            # Draw error message on screen so it's visible
            font = pygame.font.Font(None, 36)
            error_text = font.render(f"Error: {str(e)[:50]}...", True, (255, 0, 0))
            screen.blit(error_text, (20, 20))
        
        # Update display
        try:
            pygame.display.flip()
        except Exception as e:
            print(f"Error updating display: {e}")
        
        # Cap the frame rate
        clock.tick(FPS)
    
    print("Game loop ended, quitting pygame")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        print("Starting game...")
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
