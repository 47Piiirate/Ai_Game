import pygame
import json
import os
import time

class Achievement:
    """Class representing a single achievement"""
    def __init__(self, id, name, description, icon_path=None, secret=False):
        self.id = id
        self.name = name
        self.description = description
        self.unlocked = False
        self.unlock_time = None
        self.secret = secret  # If True, description is hidden until unlocked
        self.icon = None
        
        # Load icon if specified
        if icon_path:
            try:
                self.icon = pygame.image.load(icon_path).convert_alpha()
                self.icon = pygame.transform.scale(self.icon, (32, 32))
            except pygame.error:
                print(f"Could not load achievement icon: {icon_path}")
    
    def unlock(self):
        """Unlock the achievement if not already unlocked"""
        if not self.unlocked:
            self.unlocked = True
            self.unlock_time = time.time()
            return True  # Successfully unlocked
        return False  # Already unlocked
    
    def get_description(self):
        """Get achievement description (hidden if secret and locked)"""
        if self.secret and not self.unlocked:
            return "???"
        return self.description

class AchievementSystem:
    """System for tracking and displaying player achievements"""
    def __init__(self):
        self.achievements = {}
        self.recently_unlocked = []  # Queue of recently unlocked achievements
        self.display_time = 3.0  # How long to show unlock notification
        self.display_timer = 0
        self.save_path = os.path.join("saves", "achievements.json")
        
        # Load achievements
        self._create_achievements()
        self._load_achievements()
    
    def _create_achievements(self):
        """Create all game achievements"""
        self.add_achievement("first_kill", "First Blood", "Defeat your first enemy")
        self.add_achievement("explorer", "Explorer", "Discover all areas of the map")
        self.add_achievement("boss_slayer", "Boss Slayer", "Defeat the final boss")
        self.add_achievement("collector", "Collector", "Find all collectible items")
        self.add_achievement("pacifist", "Pacifist", "Complete an area without killing any enemies", secret=True)
        self.add_achievement("speedrunner", "Speed Runner", "Complete the game in under 30 minutes", secret=True)
    
    def add_achievement(self, id, name, description, icon_path=None, secret=False):
        """Add a new achievement to the system"""
        self.achievements[id] = Achievement(id, name, description, icon_path, secret)
    
    def unlock_achievement(self, achievement_id):
        """Unlock an achievement by ID"""
        if achievement_id in self.achievements and self.achievements[achievement_id].unlock():
            # Add to recently unlocked queue
            self.recently_unlocked.append(self.achievements[achievement_id])
            self.display_timer = self.display_time
            self._save_achievements()
            return True
        return False
    
    def _save_achievements(self):
        """Save achievement progress to file"""
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        
        data = {}
        for id, achievement in self.achievements.items():
            data[id] = {
                "unlocked": achievement.unlocked,
                "unlock_time": achievement.unlock_time
            }
        
        try:
            with open(self.save_path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving achievements: {e}")
    
    def _load_achievements(self):
        """Load achievement progress from file"""
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, "r") as f:
                    data = json.load(f)
                
                for id, achievement_data in data.items():
                    if id in self.achievements:
                        self.achievements[id].unlocked = achievement_data["unlocked"]
                        self.achievements[id].unlock_time = achievement_data["unlock_time"]
        except Exception as e:
            print(f"Error loading achievements: {e}")
    
    def update(self, delta_time):
        """Update achievement system (timers, notifications)"""
        if self.recently_unlocked and self.display_timer > 0:
            self.display_timer -= delta_time
            
            # Remove expired notifications
            if self.display_timer <= 0 and self.recently_unlocked:
                self.recently_unlocked.pop(0)
                if self.recently_unlocked:
                    self.display_timer = self.display_time  # Reset timer for next achievement
    
    def render(self, screen):
        """Render achievement notifications"""
        if self.recently_unlocked and self.display_timer > 0:
            achievement = self.recently_unlocked[0]
            
            # Create notification display
            notification_width = 300
            notification_height = 60
            
            # Position at top right
            x = screen.get_width() - notification_width - 10
            y = 10
            
            # Slide-in animation
            if self.display_timer > self.display_time - 0.5:
                # Slide in from right
                progress = (self.display_time - self.display_timer) / 0.5
                x = screen.get_width() - (notification_width + 10) * progress
            elif self.display_timer < 0.5:
                # Slide out to right
                progress = self.display_timer / 0.5
                x = screen.get_width() - (notification_width + 10) * progress
            
            # Draw notification background
            notification_rect = pygame.Rect(x, y, notification_width, notification_height)
            pygame.draw.rect(screen, (50, 50, 50, 200), notification_rect)
            pygame.draw.rect(screen, (255, 215, 0), notification_rect, 2)  # Gold border
            
            # Draw achievement info
            font_title = pygame.font.Font(None, 24)
            font_desc = pygame.font.Font(None, 18)
            
            title_text = font_title.render(f"Achievement Unlocked!", True, (255, 255, 255))
            name_text = font_title.render(achievement.name, True, (255, 215, 0))
            desc_text = font_desc.render(achievement.description, True, (200, 200, 200))
            
            screen.blit(title_text, (x + 10, y + 10))
            screen.blit(name_text, (x + 10, y + 30))
            screen.blit(desc_text, (x + 10, y + 50))
            
            # Draw icon if available
            if achievement.icon:
                screen.blit(achievement.icon, (x + notification_width - 42, y + 14))
    
    def get_completion_percentage(self):
        """Get the percentage of achievements unlocked"""
        if not self.achievements:
            return 0
        
        unlocked_count = sum(1 for a in self.achievements.values() if a.unlocked)
        return (unlocked_count / len(self.achievements)) * 100
    
    def check_game_progress_achievements(self, player, game_state):
        """Check game state for progress-based achievements"""
        # Example achievement checks:
        
        # Check for boss kill achievement
        if game_state.boss_defeated and not self.achievements["boss_slayer"].unlocked:
            self.unlock_achievement("boss_slayer")
        
        # Check for explorer achievement
        if len(game_state.discovered_areas) >= game_state.total_areas:
            self.unlock_achievement("explorer")
        
        # Check for collector achievement
        if len(player.collected_items) >= game_state.total_collectibles:
            self.unlock_achievement("collector")
