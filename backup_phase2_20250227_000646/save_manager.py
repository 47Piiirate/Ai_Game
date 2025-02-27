import pygame
import json
import os
import time
import datetime
from pathlib import Path
import shutil

class SaveManager:
    """Handles saving and loading game state"""
    def __init__(self):
        self.save_dir = "saves"
        self.max_slots = 3
        self.current_slot = 0
        self.auto_save_interval = 300  # seconds
        self.last_auto_save = time.time()
        
        # Ensure save directory exists
        os.makedirs(self.save_dir, exist_ok=True)
    
    def get_save_slots(self):
        """Get information about all save slots"""
        slots = []
        
        for slot in range(1, self.max_slots + 1):
            slot_info = self.get_slot_info(slot)
            slots.append(slot_info)
        
        return slots
    
    def get_slot_info(self, slot_number):
        """Get information about a specific save slot"""
        slot_path = os.path.join(self.save_dir, f"slot{slot_number}")
        slot_file = os.path.join(slot_path, "save.json")
        
        slot_info = {
            "slot": slot_number,
            "exists": False,
            "timestamp": None,
            "play_time": None,
            "player_level": None,
            "area": None,
            "thumbnail": None
        }
        
        if os.path.exists(slot_file):
            try:
                with open(slot_file, "r") as f:
                    save_data = json.load(f)
                
                slot_info["exists"] = True
                slot_info["timestamp"] = save_data.get("meta", {}).get("timestamp")
                slot_info["play_time"] = save_data.get("meta", {}).get("play_time")
                slot_info["player_level"] = save_data.get("player", {}).get("level")
                slot_info["area"] = save_data.get("level", {}).get("current_area")
                
                # Load thumbnail if exists
                thumbnail_path = os.path.join(slot_path, "thumbnail.png")
                if os.path.exists(thumbnail_path):
                    slot_info["thumbnail"] = pygame.image.load(thumbnail_path)
            except Exception as e:
                print(f"Error loading save data for slot {slot_number}: {e}")
        
        return slot_info
    
    def save_game(self, slot_number, game_state, player, level, enemies=None, screenshot=None):
        """Save game state to specified slot"""
        slot_path = os.path.join(self.save_dir, f"slot{slot_number}")
        
        # Create slot directory if it doesn't exist
        os.makedirs(slot_path, exist_ok=True)
        
        # Create save data
        save_data = {
            "meta": {
                "timestamp": time.time(),
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0",
                "play_time": game_state.play_time
            },
            "player": {
                "position": [player.rect.x, player.rect.y],
                "health": player.health,
                "max_health": player.max_health,
                "abilities": player.abilities,
                "inventory": [item.to_dict() for item in player.inventory] if hasattr(player, 'inventory') else [],
            },
            "level": {
                "current_area": level.current_area,
                "explored_areas": list(game_state.discovered_areas) if hasattr(game_state, 'discovered_areas') else [],
            }
            # Additional data would be included here
        }
        
        # Add enemies if provided
        if enemies:
            save_data["enemies"] = []
            for enemy in enemies:
                enemy_data = {
                    "type": enemy.__class__.__name__,
                    "position": [enemy.rect.x, enemy.rect.y],
                    "health": enemy.health
                }
                save_data["enemies"].append(enemy_data)
        
        # Write save data to file
        try:
            with open(os.path.join(slot_path, "save.json"), "w") as f:
                json.dump(save_data, f, indent=2)
            
            # Save screenshot thumbnail if provided
            if screenshot:
                thumbnail = pygame.transform.scale(screenshot, (160, 90))
                pygame.image.save(thumbnail, os.path.join(slot_path, "thumbnail.png"))
            
            print(f"Game saved successfully to slot {slot_number}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, slot_number):
        """Load game state from specified slot"""
        slot_path = os.path.join(self.save_dir, f"slot{slot_number}")
        save_file = os.path.join(slot_path, "save.json")
        
        if not os.path.exists(save_file):
            print(f"No save file found in slot {slot_number}")
            return None
        
        try:
            with open(save_file, "r") as f:
                save_data = json.load(f)
            
            self.current_slot = slot_number
            print(f"Game loaded successfully from slot {slot_number}")
            return save_data
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def delete_save(self, slot_number):
        """Delete save from specified slot"""
        slot_path = os.path.join(self.save_dir, f"slot{slot_number}")
        
        if os.path.exists(slot_path):
            try:
                shutil.rmtree(slot_path)
                print(f"Save in slot {slot_number} deleted successfully")
                return True
            except Exception as e:
                print(f"Error deleting save: {e}")
                return False
        else:
            print(f"No save found in slot {slot_number}")
            return False
    
    def check_auto_save(self, game_state, player, level, enemies=None, screenshot=None):
        """Check if it's time for auto-save and perform it if needed"""
        current_time = time.time()
        
        if current_time - self.last_auto_save >= self.auto_save_interval:
            print("Performing auto-save...")
            auto_save_slot = 0  # Special slot for auto-save
            success = self.save_game(auto_save_slot, game_state, player, level, enemies, screenshot)
            
            if success:
                self.last_auto_save = current_time
            
            return success
        
        return False
    
    def render_save_menu(self, screen, selected_slot=0):
        """Render the save/load menu screen"""
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Background
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(220)
        screen.blit(overlay, (0, 0))
        
        # Title
        font_title = pygame.font.Font(None, 48)
        title_text = font_title.render("Save / Load Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2, 80))
        screen.blit(title_text, title_rect)
        
        # Get save slots
        save_slots = self.get_save_slots()
        
        # Draw each slot
        slot_width = 400
        slot_height = 120
        slot_spacing = 20
        start_y = 150
        
        for i, slot in enumerate(save_slots):
            slot_rect = pygame.Rect(
                (screen_width - slot_width) // 2,
                start_y + i * (slot_height + slot_spacing),
                slot_width,
                slot_height
            )
            
            # Highlight selected slot
            color = (100, 100, 100) if i != selected_slot else (150, 150, 200)
            pygame.draw.rect(screen, color, slot_rect)
            pygame.draw.rect(screen, (200, 200, 200), slot_rect, 2)
            
            # Slot number
            font_slot = pygame.font.Font(None, 36)
            slot_text = font_slot.render(f"Slot {slot['slot']}", True, (255, 255, 255))
            screen.blit(slot_text, (slot_rect.x + 10, slot_rect.y + 10))
            
            if slot["exists"]:
                # Draw thumbnail
                if slot["thumbnail"]:
                    screen.blit(slot["thumbnail"], (slot_rect.x + 10, slot_rect.y + 40))
                
                # Draw save info
                font_info = pygame.font.Font(None, 24)
                
                timestamp_str = datetime.datetime.fromtimestamp(slot["timestamp"]).strftime("%Y-%m-%d %H:%M") if slot["timestamp"] else "Unknown"
                info_text = font_info.render(f"{timestamp_str}", True, (255, 255, 255))
                screen.blit(info_text, (slot_rect.x + 180, slot_rect.y + 40))
                
                area_text = font_info.render(f"Area: {slot['area'] or 'Unknown'}", True, (255, 255, 255))
                screen.blit(area_text, (slot_rect.x + 180, slot_rect.y + 65))
                
                time_text = font_info.render(f"Play time: {self._format_play_time(slot['play_time'])}", True, (255, 255, 255))
                screen.blit(time_text, (slot_rect.x + 180, slot_rect.y + 90))
            else:
                empty_text = font_slot.render("Empty Slot", True, (150, 150, 150))
                empty_rect = empty_text.get_rect(center=(slot_rect.centerx, slot_rect.centery))
                screen.blit(empty_text, empty_rect)
        
        # Instructions
        font_inst = pygame.font.Font(None, 24)
        inst_text = font_inst.render("↑/↓: Select Slot | Enter: Select | S: Save | L: Load | X: Delete", True, (200, 200, 200))
        inst_rect = inst_text.get_rect(center=(screen_width // 2, screen_height - 50))
        screen.blit(inst_text, inst_rect)
    
    def _format_play_time(self, seconds):
        """Format play time in seconds to HH:MM:SS"""
        if seconds is None:
            return "00:00:00"
        
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
