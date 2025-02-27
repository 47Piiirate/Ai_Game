"""
Controller system to handle input from keyboard, mouse, and controllers
"""
import pygame

class Controller:
    """
    Handles input from keyboard, mouse, and controllers
    """
    def __init__(self):
        self.keys = {}
        self.previous_keys = {}
        self.mouse_pos = (0, 0)
        self.mouse_buttons = {}
        self.previous_mouse_buttons = {}
        self.joystick = None
        
        # Try to initialize a joystick/controller if available
        self._initialize_joystick()
    
    def _initialize_joystick(self):
        """Initialize a joystick if one is available"""
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            try:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                print(f"Controller initialized: {self.joystick.get_name()}")
            except pygame.error:
                print("Error initializing controller.")
                self.joystick = None
    
    def update(self):
        """Update input state"""
        # Store previous key state
        self.previous_keys = self.keys.copy()
        
        # Get current key state
        pressed_keys = pygame.key.get_pressed()
        self.keys = {
            'up': pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w],
            'down': pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s],
            'left': pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a],
            'right': pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d],
            'jump': pressed_keys[pygame.K_SPACE],
            'attack': pressed_keys[pygame.K_z] or pressed_keys[pygame.K_j],
            'special': pressed_keys[pygame.K_x] or pressed_keys[pygame.K_k],
            'pause': pressed_keys[pygame.K_ESCAPE] or pressed_keys[pygame.K_p],
            'confirm': pressed_keys[pygame.K_RETURN] or pressed_keys[pygame.K_SPACE],
            'cancel': pressed_keys[pygame.K_ESCAPE] or pressed_keys[pygame.K_BACKSPACE],
        }
        
        # Store previous mouse button state
        self.previous_mouse_buttons = self.mouse_buttons.copy()
        
        # Get current mouse state
        self.mouse_pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()
        self.mouse_buttons = {
            'left': mouse_state[0],
            'middle': mouse_state[1],
            'right': mouse_state[2]
        }
        
        # Add controller input if available
        if self.joystick:
            # Update controller input
            try:
                # Map controller axis to movement
                x_axis = self.joystick.get_axis(0)
                y_axis = self.joystick.get_axis(1)
                
                # Add controller input to keys (with deadzone)
                deadzone = 0.2
                if abs(x_axis) > deadzone:
                    self.keys['left'] = self.keys['left'] or (x_axis < -deadzone)
                    self.keys['right'] = self.keys['right'] or (x_axis > deadzone)
                
                if abs(y_axis) > deadzone:
                    self.keys['up'] = self.keys['up'] or (y_axis < -deadzone)
                    self.keys['down'] = self.keys['down'] or (y_axis > deadzone)
                
                # Map controller buttons
                self.keys['jump'] = self.keys['jump'] or self.joystick.get_button(0)  # A/Cross button
                self.keys['attack'] = self.keys['attack'] or self.joystick.get_button(1)  # B/Circle button
                self.keys['special'] = self.keys['special'] or self.joystick.get_button(2)  # X/Square button
                self.keys['pause'] = self.keys['pause'] or self.joystick.get_button(7)  # Start button
                
            except pygame.error:
                # Controller may have been disconnected
                self.joystick = None
    
    def is_pressed(self, key):
        """Check if a key is currently pressed"""
        return self.keys.get(key, False)
    
    def is_just_pressed(self, key):
        """Check if a key was just pressed this frame"""
        return self.keys.get(key, False) and not self.previous_keys.get(key, False)
    
    def is_just_released(self, key):
        """Check if a key was just released this frame"""
        return not self.keys.get(key, False) and self.previous_keys.get(key, False)
    
    def get_movement_vector(self):
        """Get normalized movement vector from input"""
        x = 0
        y = 0
        
        if self.keys.get('right', False):
            x += 1
        if self.keys.get('left', False):
            x -= 1
        if self.keys.get('down', False):
            y += 1
        if self.keys.get('up', False):
            y -= 1
        
        # Normalize diagonal movement
        length = (x*x + y*y) ** 0.5
        if length > 0:
            x /= length
            y /= length
        
        return (x, y)
    
    def get_mouse_position(self):
        """Get current mouse position"""
        return self.mouse_pos
    
    def is_mouse_button_pressed(self, button):
        """Check if a mouse button is currently pressed"""
        return self.mouse_buttons.get(button, False)
    
    def is_mouse_button_just_pressed(self, button):
        """Check if a mouse button was just pressed this frame"""
        return (self.mouse_buttons.get(button, False) and 
                not self.previous_mouse_buttons.get(button, False))
    
    def is_mouse_button_just_released(self, button):
        """Check if a mouse button was just released this frame"""
        return (not self.mouse_buttons.get(button, False) and 
                self.previous_mouse_buttons.get(button, False))
