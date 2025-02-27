import pygame

class UI:
    """User interface rendering"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 24)  # Default font
        self.title_font = pygame.font.Font(None, 48)  # Larger font for titles
    
    def render(self, screen, player):
        """Render the game UI elements"""
        # Draw health bar
        self._draw_health_bar(screen, player)
        
        # Draw score/coins if applicable
        if hasattr(player, 'coins'):
            self._draw_coin_counter(screen, player.coins)
    
    def _draw_health_bar(self, screen, player):
        """Draw the player's health bar"""
        if hasattr(player, 'health') and hasattr(player, 'max_health'):
            # Health bar background
            bar_width = 200
            bar_height = 20
            x = 20
            y = 20
            
            # Draw background (empty bar)
            pygame.draw.rect(screen, (60, 60, 60), (x, y, bar_width, bar_height))
            
            # Calculate health percentage
            health_percentage = max(0, min(player.health / player.max_health, 1))
            
            # Draw health (filled portion)
            health_width = int(bar_width * health_percentage)
            
            # Color based on health percentage
            if health_percentage > 0.7:
                color = (0, 255, 0)  # Green
            elif health_percentage > 0.3:
                color = (255, 255, 0)  # Yellow
            else:
                color = (255, 0, 0)  # Red
                
            pygame.draw.rect(screen, color, (x, y, health_width, bar_height))
            
            # Draw border
            pygame.draw.rect(screen, (200, 200, 200), (x, y, bar_width, bar_height), 2)
            
            # Draw health text
            health_text = f"Health: {player.health}/{player.max_health}"
            text_surface = self.font.render(health_text, True, (255, 255, 255))
            screen.blit(text_surface, (x + 10, y + bar_height + 5))
    
    def _draw_coin_counter(self, screen, coins):
        """Draw the coin/score counter"""
        coin_text = f"Coins: {coins}"
        text_surface = self.font.render(coin_text, True, (255, 215, 0))  # Gold color
        screen.blit(text_surface, (self.screen_width - 150, 20))
    
    def draw_message(self, screen, message, position=None, color=(255, 255, 255)):
        """Draw a message on the screen"""
        text_surface = self.font.render(message, True, color)
        if position:
            screen.blit(text_surface, position)
        else:
            # Center the message
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(text_surface, text_rect)
