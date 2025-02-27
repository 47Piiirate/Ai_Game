import pygame
import json
import os

class DialogSystem:
    """System for displaying in-game dialog and cutscenes"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.current_dialog = None
        self.current_index = 0
        self.text_speed = 2  # Characters per frame
        self.displayed_text = ""
        self.current_char = 0
        self.waiting_for_input = False
        self.dialog_data = {}
        self.portrait_images = {}
        
        # Dialog box settings
        self.box_height = 150
        self.box_padding = 20
        self.text_color = (255, 255, 255)
        self.box_color = (0, 0, 0, 200)
        self.border_color = (100, 100, 100)
        self.portrait_size = 100
        
        # Font settings
        self.font = pygame.font.Font(None, 24)
        self.name_font = pygame.font.Font(None, 30)
        
        # Load dialog data
        self._load_dialog_data()
    
    def _load_dialog_data(self):
        """Load all dialog data from files"""
        dialog_dir = os.path.join("assets", "dialog")
        os.makedirs(dialog_dir, exist_ok=True)
        
        try:
            # Load dialog data
            dialog_path = os.path.join(dialog_dir, "dialog.json")
            if os.path.exists(dialog_path):
                with open(dialog_path, "r") as f:
                    self.dialog_data = json.load(f)
            
            # Load character portraits
            portraits_dir = os.path.join(dialog_dir, "portraits")
            if os.path.exists(portraits_dir):
                for filename in os.listdir(portraits_dir):
                    if filename.endswith((".png", ".jpg")):
                        character_name = os.path.splitext(filename)[0]
                        try:
                            portrait = pygame.image.load(os.path.join(portraits_dir, filename)).convert_alpha()
                            portrait = pygame.transform.scale(portrait, (self.portrait_size, self.portrait_size))
                            self.portrait_images[character_name] = portrait
                        except pygame.error:
                            print(f"Could not load portrait: {filename}")
        except Exception as e:
            print(f"Error loading dialog data: {e}")
    
    def start_dialog(self, dialog_id):
        """Start a specific dialog by ID"""
        if not dialog_id in self.dialog_data:
            print(f"Dialog ID '{dialog_id}' not found")
            return False
        
        self.active = True
        self.current_dialog = self.dialog_data[dialog_id]
        self.current_index = 0
        self.current_char = 0
        self.displayed_text = ""
        self.waiting_for_input = False
        
        return True
    
    def update(self):
        """Update dialog display (text animation)"""
        if not self.active or not self.current_dialog:
            return
        
        # Get current dialog entry
        if self.current_index >= len(self.current_dialog):
            self.active = False
            return
        
        current_entry = self.current_dialog[self.current_index]
        full_text = current_entry.get("text", "")
        
        # If waiting for input, don't update text
        if self.waiting_for_input:
            return
        
        # Gradually reveal text
        if self.current_char < len(full_text):
            # Add characters based on text_speed
            chars_to_add = min(self.text_speed, len(full_text) - self.current_char)
            self.displayed_text += full_text[self.current_char:self.current_char + chars_to_add]
            self.current_char += chars_to_add
            
            # Play typing sound occasionally
            # if chars_to_add > 0 and random.random() < 0.2:
            #     play_sound("typing")
        else:
            # Text is fully displayed, wait for input
            self.waiting_for_input = True
    
    def next_dialog(self):
        """Advance to next dialog entry or complete dialog if at end"""
        if not self.active:
            return
        
        # If text is still being revealed, show all of it instantly
        current_entry = self.current_dialog[self.current_index]
        full_text = current_entry.get("text", "")
        
        if not self.waiting_for_input:
            self.displayed_text = full_text
            self.current_char = len(full_text)
            self.waiting_for_input = True
            return
        
        # Move to next dialog entry
        self.current_index += 1
        
        # Check if we've reached the end
        if self.current_index >= len(self.current_dialog):
            self.active = False
            return
        
        # Reset for next entry
        self.displayed_text = ""
        self.current_char = 0
        self.waiting_for_input = False
    
    def render(self, screen):
        """Render the dialog box"""
        if not self.active:
            return
        
        if self.current_index >= len(self.current_dialog):
            return
        
        current_entry = self.current_dialog[self.current_index]
        speaker = current_entry.get("speaker", "")
        portrait_name = current_entry.get("portrait", "")
        
        # Create dialog box
        box_width = self.screen_width - (self.box_padding * 2)
        dialog_rect = pygame.Rect(
            self.box_padding,
            self.screen_height - self.box_height - self.box_padding,
            box_width,
            self.box_height
        )
        
        # Draw semi-transparent background
        dialog_surface = pygame.Surface((box_width, self.box_height), pygame.SRCALPHA)
        dialog_surface.fill(self.box_color)
        screen.blit(dialog_surface, dialog_rect.topleft)
        
        # Draw border
        pygame.draw.rect(screen, self.border_color, dialog_rect, 2)
        
        # Draw portrait if available
        portrait = self.portrait_images.get(portrait_name)
        text_start_x = self.box_padding + 10
        
        if portrait:
            portrait_rect = pygame.Rect(
                self.box_padding + 10,
                self.screen_height - self.box_height - self.box_padding + 10,
                self.portrait_size,
                self.portrait_size
            )
            screen.blit(portrait, portrait_rect.topleft)
            text_start_x = portrait_rect.right + 10
        
        # Draw speaker name if provided
        if speaker:
            name_surface = self.name_font.render(speaker, True, (255, 255, 100))
            name_rect = name_surface.get_rect()
            name_rect.topleft = (text_start_x, dialog_rect.top + 15)
            screen.blit(name_surface, name_rect.topleft)
            
            # Adjust text position to be below name
            text_rect_top = name_rect.bottom + 10
        else:
            text_rect_top = dialog_rect.top + 20
        
        # Draw text with word wrapping
        wrapped_text = self.wrap_text(self.displayed_text, box_width - (text_start_x - dialog_rect.left) - 20)
        
        text_y = text_rect_top
        for line in wrapped_text:
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (text_start_x, text_y))
            text_y += self.font.get_linesize()
        
        # Draw "continue" indicator if waiting for input
        if self.waiting_for_input:
            indicator = "▼" if pygame.time.get_ticks() % 1000 < 500 else "▽"  # Blinking indicator
            indicator_surface = self.font.render(indicator, True, (255, 255, 255))
            screen.blit(indicator_surface, (dialog_rect.right - 30, dialog_rect.bottom - 30))
    
    def wrap_text(self, text, max_width):
        """Wrap text to fit within a certain width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Test width with current word added
            test_line = ' '.join(current_line + [word])
            test_width = self.font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                # Line is full, start a new one
                if current_line:  # Avoid empty lines
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines