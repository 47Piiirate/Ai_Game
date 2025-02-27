import os
import sys
import pygame
import subprocess

def main():
    # Initialize pygame
    pygame.init()
    
    # Set up the display
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Launcher")
    
    # Fonts
    title_font = pygame.font.Font(None, 64)
    button_font = pygame.font.Font(None, 36)
    
    # Colors
    background_color = (20, 20, 40)
    button_color = (60, 60, 100)
    highlight_color = (100, 100, 180)
    text_color = (255, 255, 255)
    
    # Buttons
    start_button = pygame.Rect(300, 250, 200, 50)
    exit_button = pygame.Rect(300, 320, 200, 50)
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    # Run the main game
                    print("Starting game...")
                    subprocess.Popen([sys.executable, "main.py"])
                    running = False
                
                if exit_button.collidepoint(mouse_pos):
                    running = False
        
        # Draw background
        screen.fill(background_color)
        
        # Draw title
        title_text = title_font.render("Metroidvania Game", True, text_color)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
        
        # Draw buttons
        start_color = highlight_color if start_button.collidepoint(mouse_pos) else button_color
        exit_color = highlight_color if exit_button.collidepoint(mouse_pos) else button_color
        
        pygame.draw.rect(screen, start_color, start_button)
        pygame.draw.rect(screen, exit_color, exit_button)
        
        # Button text
        start_text = button_font.render("Start Game", True, text_color)
        exit_text = button_font.render("Exit", True, text_color)
        
        screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, 
                               start_button.y + (start_button.height - start_text.get_height()) // 2))
        screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, 
                              exit_button.y + (exit_button.height - exit_text.get_height()) // 2))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
