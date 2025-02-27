import pygame

class Camera:
    """
    Camera system for scrolling and following the player
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = 0
        self.target = None
        
    def follow(self, target):
        """
        Update camera position to follow a target entity
        """
        if target and hasattr(target, 'rect'):
            # Center camera on target with some bounds checking
            self.offset_x = target.rect.centerx - (self.width // 2)
            self.offset_y = target.rect.centery - (self.height // 2)
            
            # Optional: Add bounds checking if you have level boundaries
            # self.offset_x = max(0, min(self.offset_x, level_width - self.width))
            # self.offset_y = max(0, min(self.offset_y, level_height - self.height))
    
    def get_offset(self):
        """
        Get the current camera offset as a tuple (x, y)
        """
        return (self.offset_x, self.offset_y)
    
    def apply(self, entity):
        """
        Apply camera offset to an entity for rendering
        """
        if hasattr(entity, 'rect'):
            # Create a new rect with camera offset applied
            return pygame.Rect(
                entity.rect.x - self.offset_x,
                entity.rect.y - self.offset_y,
                entity.rect.width,
                entity.rect.height
            )
        return None
    
    def apply_rect(self, rect):
        """
        Apply camera offset to a rectangle
        """
        return pygame.Rect(
            rect.x - self.offset_x,
            rect.y - self.offset_y,
            rect.width,
            rect.height
        )
