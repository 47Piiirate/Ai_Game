import pygame
import json
import os

class GameState:
    def __init__(self):
        self.state = "menu"  # menu, playing, paused, game_over
        self.save_data = {}
        
        # Menu state
        self.menu_options = ["New Game", "Load Game", "Options", "Quit"]
        self.selected_option = 0
        
        # Create save directory if it doesn't exist
        os.makedirs("saves", exist_ok=True)
    
    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self.execute_menu_option()
    
    def execute_menu_option(self):
        if self.menu_options[self.selected_option] == "New Game":
            self.state = "playing"
        elif self.menu_options[self.selected_option] == "Load Game":
            self.load_game()
            if self.save_data:  # Only change state if we successfully loaded
                self.state = "playing"
        elif self.menu_options[self.selected_option] == "Options":
            # Options code would go here
            pass
        elif self.menu_options[self.selected_option] == "Quit":
            pygame.quit()
            import sys
            sys.exit()
    
    def render_menu(self, screen):
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw title
        font_title = pygame.font.Font(None, 74)
        title_text = font_title.render("Metroidvania Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Draw options
        font = pygame.font.Font(None, 48)
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 60))
            screen.blit(text, text_rect)
    
    def save_game(self, player, level, enemies):
        """Save game state to file"""
        save_data = {
            "player": {
                "position": [player.rect.x, player.rect.y],
                "health": player.health,
                "abilities": player.abilities,
            },
            "level": {
                "current_area": level.current_area,
            }
            # You would add more data here in a real game
        }
        
        try:
            with open("saves/save.json", "w") as f:
                json.dump(save_data, f)
            print("Game saved successfully")
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def load_game(self):
        """Load game state from file"""
        try:
            if os.path.exists("saves/save.json"):
                with open("saves/save.json", "r") as f:
                    self.save_data = json.load(f)
                print("Game loaded successfully")
            else:
                print("No save file found")
        except Exception as e:
            print(f"Error loading game: {e}")
            self.save_data = {}
