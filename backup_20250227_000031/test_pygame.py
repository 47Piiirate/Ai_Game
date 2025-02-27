"""
A simple script to test if pygame is working correctly.
"""

import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")

try:
    import pygame
    print(f"Pygame version: {pygame.__version__}")
    
    # Initialize pygame
    pygame.init()
    
    # Create a small window
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Pygame Test")
    
    # Fill the screen with a color
    screen.fill((0, 128, 255))
    
    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Pygame is working!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(200, 150))
    screen.blit(text, text_rect)
    
    pygame.display.flip()
    
    # Wait for the user to close the window
    print("Pygame initialized successfully! Close the window to exit.")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    print("Pygame test completed successfully!")

except ImportError:
    print("ERROR: Pygame is not installed in this Python environment.")
    print(f"Try installing it with: {sys.executable} -m pip install pygame")
except Exception as e:
    print(f"ERROR: {e}")
