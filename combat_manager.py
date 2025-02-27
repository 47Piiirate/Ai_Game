import pygame
import random
from particles import ParticleEffect, create_blood_splash, create_spark_burst

class CombatManager:
    """Handles combat interactions between player and enemies"""
    def __init__(self, particle_system=None, sound_manager=None):
        self.particle_system = particle_system
        self.sound_manager = sound_manager
        
        # Combat stats
        self.combo_counter = 0
        self.combo_timer = 0
        self.max_combo_time = 120  # Frames before combo resets
        self.last_hit_time = 0
        
        # Damage multipliers
        self.combo_damage_mult = {
            0: 1.0,    # Base damage
            3: 1.1,    # 3 hit combo: 10% damage boost
            5: 1.2,    # 5 hit combo: 20% damage boost
            10: 1.5,   # 10 hit combo: 50% damage boost
            20: 2.0    # 20+ hit combo: 100% damage boost
        }
        
        # Visual effects
        self.hit_effects = []
        self.critical_hit_chance = 0.1  # 10% chance for critical hit
        self.critical_hit_multiplier = 2.0
        self.hit_stop_frames = 3  # Frames to freeze on hit for impact
        self.hit_stop_timer = 0
    
    def update(self):
        """Update combat timers"""
        # Update combo timer
        if self.combo_counter > 0:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.combo_counter = 0
        
        # Update hit stop timer
        if self.hit_stop_timer > 0:
            self.hit_stop_timer -= 1
    
    def process_attack(self, attacker, targets, attack_type="normal"):
        """Process an attack from attacker to targets"""
        hits = []
        
        for target in targets:
            # Check if attack hits
            if self._check_hit(attacker, target, attack_type):
                # Calculate damage
                damage = self._calculate_damage(attacker, target, attack_type)
                
                # Apply damage
                target.take_damage(damage)
                
                # Create hit effect
                self._create_hit_effect(attacker, target, damage)
                
                # Update combo
                self._update_combo()
                
                hits.append({
                    "target": target,
                    "damage": damage,
                    "critical": damage > attacker.attack_damage
                })
                
                # Apply hit stop for impact feel
                if attack_type == "heavy":
                    self.hit_stop_timer = self.hit_stop_frames * 2
                else:
                    self.hit_stop_timer = self.hit_stop_frames
        
        return hits
    
    def _check_hit(self, attacker, target, attack_type):
        """Check if an attack hits its target"""
        if hasattr(attacker, 'attack_rect') and hasattr(target, 'rect'):
            return attacker.attack_rect.colliderect(target.rect)
        return False
    
    def _calculate_damage(self, attacker, target, attack_type):
        """Calculate damage based on attacker, target, and combat state"""
        base_damage = getattr(attacker, 'attack_damage', 10)
        
        # Apply combo multiplier
        for threshold in sorted(self.combo_damage_mult.keys(), reverse=True):
            if self.combo_counter >= threshold:
                base_damage *= self.combo_damage_mult[threshold]
                break
        
        # Apply attack type multiplier
        if attack_type == "heavy":
            base_damage *= 1.5
        elif attack_type == "dash":
            base_damage *= 1.2
        
        # Check for critical hit
        is_critical = random.random() < self.critical_hit_chance
        if is_critical:
            base_damage *= self.critical_hit_multiplier
        
        # Apply damage reduction from target defense if applicable
        if hasattr(target, 'defense'):
            base_damage = max(1, base_damage - target.defense)
        
        return int(base_damage)
    
    def _create_hit_effect(self, attacker, target, damage):
        """Create visual effects for hits"""
        if not self.particle_system:
            return
            
        # Position for effects
        hit_x = (target.rect.left + target.rect.right) // 2
        hit_y = (target.rect.top + target.rect.bottom) // 2
        
        # Create blood particles for organic targets
        if hasattr(target, 'is_organic') and target.is_organic:
            self.particle_system.add_particles(create_blood_splash(hit_x, hit_y))
        else:
            self.particle_system.add_particles(create_spark_burst(hit_x, hit_y))
        
        # Create damage number effect
        self.hit_effects.append(DamageNumber(hit_x, hit_y, damage))
        
        # Play sound effect
        if self.sound_manager:
            if damage > attacker.attack_damage:  # Critical hit
                self.sound_manager.play_sound("critical_hit")
            else:
                self.sound_manager.play_sound("hit")
    
    def _update_combo(self):
        """Update combo counter and timer after a hit"""
        self.combo_counter += 1
        self.combo_timer = self.max_combo_time
        self.last_hit_time = pygame.time.get_ticks()
    
    def render(self, screen, camera_offset):
        """Render combat effects (damage numbers, combo counter)"""
        # Render damage numbers
        for effect in self.hit_effects[:]:
            effect.update()
            effect.render(screen, camera_offset)
            
            if effect.is_expired():
                self.hit_effects.remove(effect)
        
        # Render combo counter if active
        if self.combo_counter > 1:
            font = pygame.font.Font(None, 36)
            combo_text = f"{self.combo_counter} HITS!"
            
            # Calculate size and scale based on recent hits
            scale = 1.0 + min(0.5, (pygame.time.get_ticks() - self.last_hit_time) / 200)
            text_color = (255, 255, 255)
            
            if self.combo_counter >= 10:
                text_color = (255, 255, 0)  # Yellow for 10+ combos
            if self.combo_counter >= 20:
                text_color = (255, 128, 0)  # Orange for 20+ combos
            if self.combo_counter >= 30:
                text_color = (255, 0, 0)    # Red for 30+ combos
            
            combo_surface = font.render(combo_text, True, text_color)
            scaled_width = int(combo_surface.get_width() * scale)
            scaled_height = int(combo_surface.get_height() * scale)
            scaled_surface = pygame.transform.scale(combo_surface, (scaled_width, scaled_height))
            
            screen.blit(scaled_surface, (50, 100))

class DamageNumber:
    """Floating damage number effect"""
    def __init__(self, x, y, damage, color=None):
        self.x = x
        self.y = y
        self.damage = damage
        self.lifetime = 60  # Frames
        self.velocity_y = -1.5
        self.alpha = 255
        
        # Larger text and different color for critical hits
        if damage >= 20:  # Arbitrary threshold for critical
            self.size = 24
            self.color = color or (255, 255, 0)  # Yellow for critical
        else:
            self.size = 18
            self.color = color or (255, 255, 255)  # White for normal
        
        self.font = pygame.font.Font(None, self.size)
    
    def update(self):
        """Update position and fade"""
        self.y += self.velocity_y
        self.alpha = max(0, self.alpha - 4)  # Fade out
        self.lifetime -= 1
    
    def render(self, screen, camera_offset):
        """Render the damage number"""
        # Skip rendering if fully transparent
        if self.alpha <= 0:
            return
        
        text = self.font.render(str(self.damage), True, self.color)
        
        # Apply alpha
        text.set_alpha(self.alpha)
        
        # Apply camera offset
        screen_x = int(self.x - camera_offset[0] - text.get_width() / 2)
        screen_y = int(self.y - camera_offset[1])
        
        screen.blit(text, (screen_x, screen_y))
    
    def is_expired(self):
        """Check if the damage number has expired"""
        return self.lifetime <= 0 or self.alpha <= 0
