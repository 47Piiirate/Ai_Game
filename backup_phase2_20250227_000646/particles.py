import pygame
import random
import math

class ParticleEffect:
    def __init__(self, x, y, color, size=5, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.initial_size = size
        self.lifetime = lifetime
        self.current_lifetime = lifetime
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-2, 2)
        self.gravity = 0.1
        self.fade = True
    
    def update(self):
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        
        # Shrink over time
        self.size = max(0, self.initial_size * (self.current_lifetime / self.lifetime))
        
        # Reduce lifetime
        self.current_lifetime -= 1
    
    def render(self, screen, camera_offset):
        # Apply camera offset
        x = int(self.x - camera_offset[0])
        y = int(self.y - camera_offset[1])
        
        # Calculate alpha based on remaining lifetime
        alpha = int(255 * (self.current_lifetime / self.lifetime)) if self.fade else 255
        
        # Draw the particle
        if alpha > 0 and self.size > 0:
            particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surf, 
                (*self.color, alpha),
                (self.size, self.size), 
                self.size
            )
            screen.blit(particle_surf, (x - self.size, y - self.size))
    
    def is_expired(self):
        return self.current_lifetime <= 0

class BloodEffect(ParticleEffect):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 0, 0), random.randint(2, 5), random.randint(20, 40))

class SparkEffect(ParticleEffect):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 255, 0), random.randint(1, 3), random.randint(10, 20))
        self.velocity_x = random.uniform(-3, 3)
        self.velocity_y = random.uniform(-3, 3)
        self.gravity = 0.05

class DustEffect(ParticleEffect):
    def __init__(self, x, y):
        super().__init__(x, y, (150, 150, 150), random.randint(2, 4), random.randint(30, 50))
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-0.5, 0)
        self.gravity = 0.03

class FireEffect(ParticleEffect):
    """Fire particle with upward movement and color transition"""
    def __init__(self, x, y):
        size = random.randint(3, 8)
        lifetime = random.randint(20, 40)
        color = (255, random.randint(100, 200), 0)  # Orange-red
        
        super().__init__(x, y, color, size, lifetime)
        self.velocity_x = random.uniform(-0.5, 0.5)
        self.velocity_y = random.uniform(-1.5, -0.5)  # Always moves up
        self.gravity = -0.01  # Slight lift
    
    def update(self):
        super().update()
        # Transition to darker color as it burns out
        if self.current_lifetime < self.lifetime / 2:
            fade_ratio = self.current_lifetime / (self.lifetime / 2)
            self.color = (
                max(0, int(255 * fade_ratio)),
                max(0, int(self.color[1] * fade_ratio)),
                0
            )

class WaterEffect(ParticleEffect):
    """Water droplet with physics"""
    def __init__(self, x, y):
        size = random.randint(2, 5)
        lifetime = random.randint(30, 60)
        shade = random.randint(150, 255)
        color = (0, random.randint(100, 200), shade)  # Blue shade
        
        super().__init__(x, y, color, size, lifetime)
        self.velocity_x = random.uniform(-1.0, 1.0)
        self.velocity_y = random.uniform(-0.5, 2.0)  # Can go up or down
        self.gravity = 0.15
        self.bounce_factor = 0.6  # Bounces when hitting surface
        self.ground_y = 500  # Default ground level (should be externally set)
    
    def update(self):
        super().update()
        
        # Check for bounce on ground
        if self.y > self.ground_y:
            self.y = self.ground_y
            if abs(self.velocity_y) > 0.5:  # Only bounce if moving fast enough
                self.velocity_y = -self.velocity_y * self.bounce_factor
            else:
                self.velocity_y = 0
                self.velocity_x *= 0.9  # Friction when sliding on ground

class ParticleSystem:
    """A system to manage multiple particle effects"""
    def __init__(self):
        self.particles = []
        self.emitters = []

    def add_particles(self, particles):
        """Add particles to the system"""
        if isinstance(particles, list):
            self.particles.extend(particles)
        else:
            self.particles.append(particles)

    def add_emitter(self, emitter):
        """Add an emitter to the system"""
        self.emitters.append(emitter)

    def update(self):
        """Update all particles and emitters"""
        # Update existing particles
        for particle in self.particles[:]:
            particle.update()
            if particle.is_expired():
                self.particles.remove(particle)
        
        # Update emitters and generate new particles
        for emitter in self.emitters[:]:
            new_particles = emitter.update()
            if new_particles:
                self.add_particles(new_particles)
            
            if emitter.is_expired():
                self.emitters.remove(emitter)

    def render(self, screen, camera_offset):
        """Render all particles"""
        for particle in self.particles:
            particle.render(screen, camera_offset)

class ParticleEmitter:
    """Continuously generates particles based on parameters"""
    def __init__(self, x, y, particle_type, rate=1, duration=None, variation=0.2):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.rate = rate  # Particles per frame
        self.duration = duration  # None means infinite
        self.variation = variation  # Position variation
        self.timer = 0
        self.particle_count = 0
    
    def update(self):
        """Update emitter and generate particles if needed"""
        if self.duration is not None:
            self.duration -= 1
        
        self.timer += self.rate
        new_particles = []
        
        while self.timer >= 1:
            # Create new particle with variation in position
            var_x = self.x + random.uniform(-self.variation, self.variation) * 10
            var_y = self.y + random.uniform(-self.variation, self.variation) * 10
            
            if self.particle_type == "blood":
                new_particles.append(BloodEffect(var_x, var_y))
            elif self.particle_type == "spark":
                new_particles.append(SparkEffect(var_x, var_y))
            elif self.particle_type == "dust":
                new_particles.append(DustEffect(var_x, var_y))
            elif self.particle_type == "fire":
                new_particles.append(FireEffect(var_x, var_y))
            elif self.particle_type == "water":
                new_particles.append(WaterEffect(var_x, var_y))
            
            self.timer -= 1
            self.particle_count += 1
        
        return new_particles
    
    def is_expired(self):
        """Check if the emitter has reached its duration"""
        return self.duration is not None and self.duration <= 0

def create_particle_explosion(x, y, color, count=10):
    particles = []
    for i in range(count):
        particles.append(ParticleEffect(x, y, color))
    return particles

def create_blood_splash(x, y, count=8):
    particles = []
    for i in range(count):
        particles.append(BloodEffect(x, y))
    return particles

def create_spark_burst(x, y, count=15):
    particles = []
    for i in range(count):
        particles.append(SparkEffect(x, y))
    return particles
