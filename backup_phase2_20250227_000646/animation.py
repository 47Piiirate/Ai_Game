import pygame

class Animation:
    def __init__(self, frames, frame_duration=5, loop=True):
        """
        Initialize an animation
        
        Args:
            frames: List of pygame surfaces for each animation frame
            frame_duration: Number of game ticks each frame should display
            loop: Whether the animation should loop
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        
        self.current_frame_index = 0
        self.timer = 0
        self.finished = False
    
    def update(self):
        """Update the animation state"""
        if self.finished:
            return
            
        self.timer += 1
        
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame_index += 1
            
            if self.current_frame_index >= len(self.frames):
                if self.loop:
                    self.current_frame_index = 0
                else:
                    self.current_frame_index = len(self.frames) - 1
                    self.finished = True
    
    def reset(self):
        """Reset the animation to the first frame"""
        self.current_frame_index = 0
        self.timer = 0
        self.finished = False
    
    def get_current_frame(self):
        """Get the current frame of the animation"""
        return self.frames[self.current_frame_index]
    
    def is_finished(self):
        """Check if a non-looping animation has finished"""
        return self.finished

class AnimatedSprite:
    def __init__(self, x, y):
        """Base class for objects with animations"""
        self.animations = {}
        self.current_animation = None
        self.rect = pygame.Rect(x, y, 0, 0)
        self.facing_right = True
    
    def add_animation(self, name, animation):
        """Add an animation to this sprite"""
        self.animations[name] = animation
        
        # Set first animation as current if none is set
        if self.current_animation is None:
            self.current_animation = name
    
    def play_animation(self, name, reset=True):
        """Change to a different animation"""
        if name in self.animations:
            # Only reset if animation changes or reset is forced
            if self.current_animation != name or reset:
                self.current_animation = name
                self.animations[name].reset()
    
    def update_animation(self):
        """Update the current animation"""
        if self.current_animation:
            self.animations[self.current_animation].update()
    
    def get_current_frame(self):
        """Get the current animation frame"""
        if self.current_animation:
            image = self.animations[self.current_animation].get_current_frame()
            
            # Flip the image if facing left
            if not self.facing_right:
                image = pygame.transform.flip(image, True, False)
            
            return image
        return None
