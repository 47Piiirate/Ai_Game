import pygame
from enemy import Enemy, Boss
import random
import room
import item
from collectible import Collectible

class Game:
    def __init__(self, level, player, camera, ui, sound_manager=None, asset_manager=None):
        self.level = level
        self.player = player
        self.camera = camera
        self.ui = ui
        self.sound_manager = sound_manager
        self.asset_manager = asset_manager
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.current_level_name = "starting_area"
        self.game_state = "playing"  # playing, paused, game_over, level_transition
        self.transition_timer = 0
        self.spawn_enemies()
        
        # Initialize any collectibles from level
        self.collectibles = []
        self._init_collectibles()
    
    def _init_collectibles(self):
        """Initialize collectibles from level data"""
        self.collectibles = []
        for collectible_data in self.level.collectibles:
            collectible = Collectible(
                collectible_data["rect"].centerx, 
                collectible_data["rect"].centery, 
                collectible_data["type"],
                asset_manager=self.asset_manager  # Pass asset manager
            )
            self.collectibles.append(collectible)
        
    def spawn_enemies(self):
        # Clear existing enemies
        self.enemies = []
        
        # Add some basic enemies - different number based on level
        if self.current_level_name == "starting_area":
            enemy_count = 3
        elif self.current_level_name == "underground_cave":
            enemy_count = 5
        else:
            enemy_count = 1
            
        for i in range(enemy_count):
            x = random.randint(100, 1000)
            y = random.randint(100, 400)
            self.enemies.append(Enemy(x, y, asset_manager=self.asset_manager))
        
        # Add a boss at a specific location
        if self.current_level_name == "boss_chamber":
            self.enemies.append(Boss(600, 300, asset_manager=self.asset_manager))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.game_state == "playing":
                    self.game_state = "paused"
                elif self.game_state == "paused":
                    self.game_state = "playing"
            
            # Attack on mouse click or key
            if event.key == pygame.K_z:
                self.player.attack()
                if self.sound_manager:
                    self.sound_manager.play_sound("attack")
            
            # Parry/deflect on key
            if event.key == pygame.K_x:
                self.player.parry()
                if self.sound_manager:
                    self.sound_manager.play_sound("parry")
                
            # Dash on key
            if event.key == pygame.K_c:
                self.player.dash()
                if self.sound_manager:
                    self.sound_manager.play_sound("dash")
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.player.attack()
                if self.sound_manager:
                    self.sound_manager.play_sound("attack")
    
    def update(self, keys):
        if self.game_state == "playing":
            # Update player
            self.player.update(keys, self.level)
            
            # Check for level transition
            transition = self.level.check_transitions(self.player.rect)
            if transition:
                target_level, spawn_x, spawn_y = transition
                self.change_level(target_level, spawn_x, spawn_y)
                return
            
            # Update camera to follow player
            self.camera.update(self.player)
            
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.update(self.player)
                
                # Check for player attacks hitting enemies
                if self.player.is_attacking and self.player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.attack_damage)
                    if self.sound_manager:
                        if isinstance(enemy, Boss):
                            self.sound_manager.play_sound("boss_hit")
                        else:
                            self.sound_manager.play_sound("hit")
                    
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        # Add kill effects (particles)
                        if self.sound_manager:
                            self.sound_manager.play_sound("death")
                
                # Check for enemy attacks hitting player
                if enemy.is_attacking and enemy.attack_rect.colliderect(self.player.rect):
                    if self.player.is_parrying:
                        enemy.take_damage(10)  # Successful parry damages enemy
                        self.particles.extend(self.player.create_parry_particles())
                        if self.sound_manager:
                            self.sound_manager.play_sound("parry")
                    else:
                        self.player.take_damage(enemy.attack_damage)
                        if self.sound_manager:
                            self.sound_manager.play_sound("hit")
            
            # Update collectibles
            for collectible in self.collectibles[:]:
                collectible.update()
                if collectible.collect(self.player):
                    self.collectibles.remove(collectible)
                    if self.sound_manager:
                        self.sound_manager.play_sound("collect")
            
            # Update projectiles
            for projectile in self.projectiles[:]:
                projectile.update()
                if projectile.is_expired():
                    self.projectiles.remove(projectile)
            
            # Update particles
            for particle in self.particles[:]:
                particle.update()
                if particle.is_expired():
                    self.particles.remove(particle)
            
            # Check if player is dead
            if not self.player.is_alive():
                self.game_state = "game_over"
                
        elif self.game_state == "level_transition":
            # Handle level transition animation
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                self.game_state = "playing"
    
    def change_level(self, target_level, spawn_x, spawn_y):
        """Change to a new level and position the player"""
        print(f"Transitioning to {target_level}")
        
        # Set transition state
        self.game_state = "level_transition"
        self.transition_timer = 30  # frames for transition effect
        
        # Load the new level
        self.level.load_level(target_level)
        self.current_level_name = target_level
        
        # Set player position
        self.player.rect.x = spawn_x
        self.player.rect.y = spawn_y
        
        # Reset camera
        self.camera.target_x = spawn_x - (self.camera.width / 2)
        self.camera.target_y = spawn_y - (self.camera.height / 2)
        self.camera.x = self.camera.target_x
        self.camera.y = self.camera.target_y
        
        # Spawn enemies for the new level
        self.spawn_enemies()
        
        # Initialize collectibles from the new level
        self._init_collectibles()
        
        # Play appropriate sound if available
        if self.sound_manager:
            if target_level == "underground_cave":
                self.sound_manager.play_music("cave")
            elif target_level == "boss_chamber":
                self.sound_manager.play_music("boss")
            else:
                self.sound_manager.play_music("main_area")
    
    def render(self, screen):
        # Apply camera offset to everything we render
        camera_offset = self.camera.get_offset()
        
        # Render the level
        self.level.render(screen, camera_offset)
        
        # Render enemies
        for enemy in self.enemies:
            enemy.render(screen, camera_offset)
        
        # Render collectibles
        for collectible in self.collectibles:
            collectible.render(screen, camera_offset)
        
        # Render player
        self.player.render(screen, camera_offset)
        
        # Render projectiles
        for projectile in self.projectiles:
            projectile.render(screen, camera_offset)
        
        # Render particles
        for particle in self.particles:
            particle.render(screen, camera_offset)
        
        # Render UI (no camera offset for UI)
        self.ui.render(screen, self.player)
        
        # Render level transition effect
        if self.game_state == "level_transition":
            # Create fade effect
            overlay = pygame.Surface((screen.get_width(), screen.get_height()))
            alpha = min(255, (self.transition_timer / 30) * 255)
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Display level name
            if self.transition_timer < 15:  # Show name in second half of transition
                font = pygame.font.Font(None, 36)
                level_text = font.render(f"Entering: {self.current_level_name.replace('_', ' ').title()}", 
                                      True, (255, 255, 255))
                text_rect = level_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
                screen.blit(level_text, text_rect)
        
        # Render pause or game over screen
        if self.game_state == "paused":
            self.render_pause_screen(screen)
        elif self.game_state == "game_over":
            self.render_game_over_screen(screen)
    
    def render_pause_screen(self, screen):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
    
    def render_game_over_screen(self, screen):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(192)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
