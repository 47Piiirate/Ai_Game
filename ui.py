import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.ability_icons = {}
        # Add default ability icon images (placeholder)
        self.ability_icons['double_jump'] = self.create_ability_icon((0, 255, 0))
        self.ability_icons['wall_jump'] = self.create_ability_icon((0, 0, 255))
        self.ability_icons['dash'] = self.create_ability_icon((255, 0, 255)) 
        self.ability_icons['charged_attack'] = self.create_ability_icon((255, 255, 0))
    
    def create_ability_icon(self, color):
        # Create a placeholder icon with the given color
        icon = pygame.Surface((30, 30))
        icon.fill(color)
        pygame.draw.rect(icon, (255, 255, 255), icon.get_rect(), 2)
        return icon
    
    def render(self, screen, player):
        # Draw health bar
        self.draw_health_bar(screen, player)
        
        # Draw stamina bar
        self.draw_stamina_bar(screen, player)
        
        # Draw ability icons
        self.draw_ability_icons(screen, player)
        
        # Show debug info
        if hasattr(player, 'abilities'):
            # Render unlocked abilities text
            unlocked = [name for name, has in player.abilities.items() if has]
            if unlocked:
                ability_text = f"Abilities: {', '.join(unlocked)}"
            else:
                ability_text = "Abilities: None"
            text_surf = self.font.render(ability_text, True, (255, 255, 255))
            screen.blit(text_surf, (10, 60))
    
    def draw_health_bar(self, screen, player):
        # Health bar background
        health_bar_width = 200
        health_bar_height = 20
        health_bar_bg = pygame.Rect(10, 10, health_bar_width, health_bar_height)
        pygame.draw.rect(screen, (100, 0, 0), health_bar_bg)
        
        # Health bar fill
        fill_width = int((player.health / player.max_health) * health_bar_width)
        health_bar_fill = pygame.Rect(10, 10, fill_width, health_bar_height)
        pygame.draw.rect(screen, (255, 0, 0), health_bar_fill)
        
        # Health bar outline
        pygame.draw.rect(screen, (255, 255, 255), health_bar_bg, 2)
        
        # Health text
        health_text = f"{player.health}/{player.max_health}"
        text_surf = self.font.render(health_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midright=(10 + health_bar_width - 5, 10 + health_bar_height // 2))
        screen.blit(text_surf, text_rect)
    
    def draw_stamina_bar(self, screen, player):
        # Stamina bar background
        stamina_bar_width = 200
        stamina_bar_height = 10
        stamina_bar_bg = pygame.Rect(10, 35, stamina_bar_width, stamina_bar_height)
        pygame.draw.rect(screen, (50, 50, 50), stamina_bar_bg)
        
        # Stamina bar fill
        fill_width = int((player.stamina / player.max_stamina) * stamina_bar_width)
        stamina_bar_fill = pygame.Rect(10, 35, fill_width, stamina_bar_height)
        pygame.draw.rect(screen, (0, 255, 255), stamina_bar_fill)
        
        # Stamina bar outline
        pygame.draw.rect(screen, (255, 255, 255), stamina_bar_bg, 1)
    
    def draw_ability_icons(self, screen, player):
        # Draw ability icons at bottom of screen
        icon_spacing = 40
        start_x = 10
        start_y = screen.get_height() - 40
        
        # Draw each ability icon
        for i, (ability_name, has_ability) in enumerate(player.abilities.items()):
            icon_x = start_x + (i * icon_spacing)
            icon_rect = pygame.Rect(icon_x, start_y, 30, 30)
            
            # Draw darker if ability not acquired
            if has_ability:
                screen.blit(self.ability_icons[ability_name], icon_rect)
            else:
                # Draw gray silhouette if not unlocked
                gray_icon = self.ability_icons[ability_name].copy()
                gray_icon.fill((50, 50, 50))
                screen.blit(gray_icon, icon_rect)
            
            # Draw border
            pygame.draw.rect(screen, (255, 255, 255), icon_rect, 1)
