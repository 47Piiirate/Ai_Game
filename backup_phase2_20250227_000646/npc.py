import pygame
import random
import json
import os
from dialog import DialogSystem

class NPC:
    """Base class for non-player characters"""
    def __init__(self, x, y, name, npc_id, dialog_key=None):
        self.x = x
        self.y = y
        self.name = name
        self.npc_id = npc_id
        self.dialog_key = dialog_key
        
        # Create default appearance
        self.width = 40
        self.height = 70
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Default color for NPCs that don't have images
        self.color = (0, 200, 100)  # Green default
        self.image = None
        
        # Interaction settings
        self.interaction_radius = 80  # How close player needs to be to interact
        self.can_interact = True
        self.quest_giver = False
        self.shop_keeper = False
        
        # Animation variables
        self.facing_right = True
        self.idle_timer = 0
        self.idle_direction_change = random.randint(60, 120)  # Frames before changing idle direction
        self.idle_move_speed = 0.2
        self.idle_direction = 0  # -1 = left, 0 = stand, 1 = right
    
    def load_image(self, image_path):
        """Load NPC image"""
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error:
            print(f"Could not load NPC image: {image_path}")
            # Create a placeholder image
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill(self.color)
    
    def update(self, player=None):
        """Update NPC state"""
        # Basic idle animation
        self.idle_timer += 1
        if self.idle_timer >= self.idle_direction_change:
            self.idle_timer = 0
            self.idle_direction_change = random.randint(60, 120)
            self.idle_direction = random.choice([-1, 0, 0, 0, 1])  # Favor standing still
        
        # Apply idle movement
        if self.idle_direction != 0:
            new_x = self.x + self.idle_direction * self.idle_move_speed
            # Check if movement would go out of bounds
            if 0 <= new_x <= 1280 - self.width:  # assuming 1280 is screen width
                self.x = new_x
                self.rect.x = int(self.x)
            else:
                self.idle_direction *= -1  # Reverse direction if hitting boundary
            
            # Update facing direction
            if self.idle_direction > 0:
                self.facing_right = True
            elif self.idle_direction < 0:
                self.facing_right = False
    
    def render(self, screen, camera_offset):
        """Render NPC to the screen"""
        npc_rect = self.rect.copy()
        npc_rect.x -= camera_offset[0]
        npc_rect.y -= camera_offset[1]
        
        if self.image:
            # Flip image based on facing direction
            if self.facing_right:
                screen.blit(self.image, npc_rect.topleft)
            else:
                flipped_image = pygame.transform.flip(self.image, True, False)
                screen.blit(flipped_image, npc_rect.topleft)
        else:
            # Draw a rectangle if no image
            pygame.draw.rect(screen, self.color, npc_rect)
        
        # Draw name above NPC
        font = pygame.font.Font(None, 20)
        name_text = font.render(self.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(centerx=npc_rect.centerx, bottom=npc_rect.top - 5)
        screen.blit(name_text, name_rect)
        
        # Draw interaction indicator if player is within range
        if self.can_interact_with_player:
            indicator_y = npc_rect.top - 20
            indicator_text = font.render("Press E to talk", True, (255, 255, 0))
            indicator_rect = indicator_text.get_rect(centerx=npc_rect.centerx, bottom=indicator_y)
            screen.blit(indicator_text, indicator_rect)
    
    def check_interaction(self, player):
        """Check if player can interact with this NPC"""
        self.can_interact_with_player = False
        
        # Calculate distance to player
        player_center = player.rect.center
        npc_center = self.rect.center
        
        dx = player_center[0] - npc_center[0]
        dy = player_center[1] - npc_center[1]
        distance = (dx**2 + dy**2)**0.5
        
        # Check if player is within interaction radius
        if distance <= self.interaction_radius:
            self.can_interact_with_player = True
            return True
        
        return False
    
    def interact(self, player, dialog_system, quest_manager=None):
        """Handle player interaction with NPC"""
        if self.dialog_key:
            # Start dialog if available
            dialog_system.start_dialog(self.dialog_key)
            return True
        
        return False
    
    def to_dict(self):
        """Convert NPC data to dictionary for saving"""
        return {
            "id": self.npc_id,
            "name": self.name,
            "position": [self.x, self.y],
            "dialog_key": self.dialog_key,
            "quest_giver": self.quest_giver,
            "shop_keeper": self.shop_keeper
        }

class QuestGiverNPC(NPC):
    """NPC that can give quests to the player"""
    def __init__(self, x, y, name, npc_id, dialog_key=None):
        super().__init__(x, y, name, npc_id, dialog_key)
        self.quest_giver = True
        self.available_quests = []  # List of quest IDs this NPC can give
        self.completion_quests = []  # List of quest IDs this NPC receives for completion
        self.color = (200, 150, 0)  # Gold color for quest givers
    
    def add_quest(self, quest_id, is_completion=False):
        """Add a quest to this NPC's available quests"""
        if is_completion:
            self.completion_quests.append(quest_id)
        else:
            self.available_quests.append(quest_id)
    
    def interact(self, player, dialog_system, quest_manager=None):
        """Handle player interaction with quest giver NPC"""
        if not quest_manager:
            return super().interact(player, dialog_system)
        
        # Check for quest completion first
        for quest_id in self.completion_quests:
            if quest_id in quest_manager.active_quests and quest_manager.active_quests[quest_id].is_complete():
                # Complete the quest
                rewards = quest_manager.complete_quest(quest_id)
                
                # Find and start completion dialog if available
                completion_dialog = f"{quest_id}_complete"
                if completion_dialog in dialog_system.dialog_data:
                    dialog_system.start_dialog(completion_dialog)
                    return True
        
        # Check for available quests
        for quest_id in self.available_quests:
            # Check if quest is available (prerequisites met)
            if quest_id not in quest_manager.active_quests and quest_id not in quest_manager.completed_quests:
                # Check if quest exists in database and prerequisites are met
                available_quests = quest_manager.get_available_quests()
                for quest in available_quests:
                    if quest.quest_id == quest_id:
                        # Start quest dialog
                        dialog_key = f"{quest_id}_start"
                        if dialog_key in dialog_system.dialog_data:
                            dialog_system.start_dialog(dialog_key)
                        else:
                            # Use default dialog if specific one not found
                            super().interact(player, dialog_system)
                        
                        # Start the quest
                        quest_manager.start_quest(quest_id)
                        return True
        
        # If no quests are available, use normal dialog
        return super().interact(player, dialog_system)
    
    def render(self, screen, camera_offset):
        """Render quest giver NPC with quest indicator"""
        super().render(screen, camera_offset)
        
        # Add quest marker above NPC if they have available quests
        npc_rect = self.rect.copy()
        npc_rect.x -= camera_offset[0]
        npc_rect.y -= camera_offset[1]
        
        if self.available_quests or self.completion_quests:
            # Draw a yellow '!' for available quests
            font = pygame.font.Font(None, 30)
            quest_marker = font.render("!", True, (255, 255, 0))
            marker_rect = quest_marker.get_rect(centerx=npc_rect.centerx, bottom=npc_rect.top - 25)
            
            # Draw yellow circle behind the exclamation mark
            circle_radius = 10
            pygame.draw.circle(
                screen, 
                (255, 255, 0), 
                (marker_rect.centerx, marker_rect.centery), 
                circle_radius
            )
            pygame.draw.circle(
                screen, 
                (0, 0, 0), 
                (marker_rect.centerx, marker_rect.centery), 
                circle_radius, 
                2
            )
            
            # Draw the exclamation mark
            screen.blit(quest_marker, marker_rect)

class ShopkeeperNPC(NPC):
    """NPC that sells items to the player"""
    def __init__(self, x, y, name, npc_id, dialog_key=None):
        super().__init__(x, y, name, npc_id, dialog_key)
        self.shop_keeper = True
        self.inventory = []  # List of items for sale
        self.color = (0, 100, 200)  # Blue color for shopkeepers
        
    def add_item_for_sale(self, item, price):
        """Add an item to the shopkeeper's inventory"""
        self.inventory.append({"item": item, "price": price})
    
    def interact(self, player, dialog_system, quest_manager=None):
        """Handle player interaction with shopkeeper NPC"""
        # Open shop interface instead of normal dialog
        # For now, just use normal dialog
        return super().interact(player, dialog_system)
