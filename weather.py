import pygame
import random
from particles import ParticleSystem, ParticleEmitter

class WeatherSystem:
    """System for handling weather effects like rain, snow, etc."""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particle_system = ParticleSystem()
        self.current_weather = None
        self.intensity = 0.0  # 0.0 to 1.0
        self.transition_speed = 0.01
        self.target_intensity = 0.0
        self.weather_emitters = []
    
    def set_weather(self, weather_type, intensity=1.0, transition=True):
        """Set the current weather type and intensity"""
        if weather_type == self.current_weather and intensity == self.intensity:
            return
        
        # Set target intensity for smooth transition
        self.target_intensity = intensity
        
        # If weather type is changing, clear existing emitters
        if weather_type != self.current_weather:
            self.weather_emitters = []
            self.current_weather = weather_type
            if not transition:
                self.intensity = intensity
            
            # Create appropriate emitters for the weather
            if weather_type == "rain":
                self._setup_rain_emitters()
            elif weather_type == "snow":
                self._setup_snow_emitters()
            elif weather_type == "fog":
                self._setup_fog_emitters()
            elif weather_type == "thunder":
                self._setup_thunder_emitters()
    
    def _setup_rain_emitters(self):
        """Create rain particle emitters"""
        for i in range(10):
            emitter = ParticleEmitter(
                random.randint(0, self.screen_width),
                -20,  # Above screen
                "water",
                rate=0.3,
                variation=1.0
            )
            self.weather_emitters.append(emitter)
            self.particle_system.add_emitter(emitter)
    
    def _setup_snow_emitters(self):
        """Create snow particle emitters"""
        # Similar to rain but with different particles and settings
        pass
    
    def _setup_fog_emitters(self):
        """Create fog particle emitters"""
        # Create fog effect
        pass
    
    def _setup_thunder_emitters(self):
        """Create thunder effect (flashes and intense rain)"""
        # Setup rain + occasional screen flash
        self._setup_rain_emitters()
        # Add thunder logic
    
    def update(self, camera_position):
        """Update the weather system"""
        # Update intensity with smooth transition
        if self.intensity < self.target_intensity:
            self.intensity = min(self.target_intensity, self.intensity + self.transition_speed)
        elif self.intensity > self.target_intensity:
            self.intensity = max(self.target_intensity, self.intensity - self.transition_speed)
        
        # Adjust emitter positions based on camera
        for emitter in self.weather_emitters:
            # Keep emitters in visible area
            emitter.x = camera_position[0] + random.randint(0, self.screen_width)
        
        # Update particle system
        self.particle_system.update()
        
        # Handle special weather effects
        if self.current_weather == "thunder" and random.random() < 0.005 * self.intensity:
            self._trigger_thunder_flash()
    
    def _trigger_thunder_flash(self):
        """Create a lightning flash effect"""
        # Would be implemented to create a flash overlay or screen effect
        pass
    
    def render(self, screen, camera_offset):
        """Render all weather particles and effects"""
        # Add fog overlay if applicable
        if self.current_weather == "fog":
            fog_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            fog_surface.fill((200, 200, 200, int(50 * self.intensity)))
            screen.blit(fog_surface, (0, 0))
        
        # Render all particles
        self.particle_system.render(screen, camera_offset)
