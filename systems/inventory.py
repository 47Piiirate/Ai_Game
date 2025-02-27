import pygame
import json
import os

class Item:
    """Base class for all inventory items"""
    def __init__(self, item_id, name, description, icon_path=None, stackable=False, max_stack=1):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.stackable = stackable
        self.max_stack = max_stack
        self.count = 1
        self.icon = None
        self.equipped = False
        
        # Load icon if specified
        if icon_path and os.path.exists(icon_path):
            try:
                self.icon = pygame.image.load(icon_path).convert_alpha()
                self.icon = pygame.transform.scale(self.icon, (32, 32))
            except pygame.error:
                print(f"Could not load item icon: {icon_path}")
                self.icon = self._create_default_icon()
        else:
            self.icon = self._create_default_icon()
    
    def _create_default_icon(self):
        """Create a default icon when image can't be loaded"""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        icon.fill((100, 100, 100))
        pygame.draw.rect(icon, (200, 200, 200), icon.get_rect(), 2)
        return icon
    
    def use(self, player):
        """Use this item (to be overridden by subclasses)"""
        print(f"Using {self.name}")
        return False  # Return True if item should be consumed
    
    def to_dict(self):
        """Convert item to dictionary for saving"""
        return {
            "id": self.item_id,
            "count": self.count,
            "equipped": self.equipped
        }
    
    @staticmethod
    def from_dict(data, item_database):
        """Create an item from saved data"""
        item_id = data.get("id")
        if item_id in item_database:
            item = item_database[item_id].copy()
            item.count = data.get("count", 1)
            item.equipped = data.get("equipped", False)
            return item
        return None
    
    def copy(self):
        """Create a copy of this item"""
        new_item = Item(self.item_id, self.name, self.description, None, self.stackable, self.max_stack)
        new_item.icon = self.icon
        new_item.count = 1  # Reset count on copy
        return new_item

class HealthPotion(Item):
    """Health potion that restores player health"""
    def __init__(self, heal_amount=30):
        super().__init__(
            "health_potion",
            "Health Potion",
            f"Restores {heal_amount} health when used.",
            stackable=True,
            max_stack=10
        )
        self.heal_amount = heal_amount
    
    def use(self, player):
        if player.health < player.max_health:
            player.heal(self.heal_amount)
            print(f"Used health potion. Healed for {self.heal_amount}")
            return True  # Consume the potion
        else:
            print("Health is already full!")
            return False  # Don't consume if full health

class EquippableItem(Item):
    """Base class for items that can be equipped"""
    def __init__(self, item_id, name, description, icon_path=None, slot="accessory"):
        super().__init__(item_id, name, description, icon_path, stackable=False)
        self.slot = slot  # Equipment slot: weapon, armor, accessory, etc.
    
    def equip(self, player):
        """Equip this item to the player"""
        self.equipped = True
        print(f"Equipped {self.name}")
        return True
    
    def unequip(self, player):
        """Unequip this item from the player"""
        self.equipped = False
        print(f"Unequipped {self.name}")
        return True

class Inventory:
    """Player inventory system"""
    def __init__(self, size=24):
        self.items = []
        self.size = size
        self.selected_index = 0
        self.visible = False
        
        # UI settings
        self.slot_size = 40
        self.slot_padding = 5
        self.slots_per_row = 8
        
        # Tooltip
        self.show_tooltip = False
        self.tooltip_item = None
    
    def add_item(self, item):
        """Add an item to the inventory"""
        # Check if item is stackable and if we have it already
        if item.stackable:
            for existing_item in self.items:
                if existing_item.item_id == item.item_id and existing_item.count < existing_item.max_stack:
                    # Stack with existing item
                    space_left = existing_item.max_stack - existing_item.count
                    amount_to_add = min(space_left, item.count)
                    existing_item.count += amount_to_add
                    item.count -= amount_to_add
                    
                    # If we've added all of the new items, we're done
                    if item.count == 0:
                        return True
        
        # If we get here, either the item isn't stackable or we couldn't stack all of them
        if len(self.items) < self.size:
            self.items.append(item)
            return True
        else:
            print("Inventory is full!")
            return False
    
    def remove_item(self, index, count=1):
        """Remove item at the specified index"""
        if 0 <= index < len(self.items):
            item = self.items[index]
            if item.count > count:
                item.count -= count
                return True
            else:
                self.items.pop(index)
                return True
        return False
    
    def use_item(self, index, player):
        """Use the item at the specified index"""
        if 0 <= index < len(self.items):
            item = self.items[index]
            if item.use(player):
                # Item was consumed
                item.count -= 1
                if item.count <= 0:
                    self.items.pop(index)
                return True
        return False
    
    def toggle_visibility(self):
        """Toggle inventory visibility"""
        self.visible = not self.visible
        self.show_tooltip = False  # Hide tooltip when toggling
    
    def render(self, screen):
        """Render the inventory UI"""
        if not self.visible:
            return
        
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate inventory dimensions
        inventory_width = (self.slot_size + self.slot_padding) * self.slots_per_row + self.slot_padding
        rows = (self.size + self.slots_per_row - 1) // self.slots_per_row  # Ceiling division
        inventory_height = (self.slot_size + self.slot_padding) * rows + self.slot_padding
        
        # Center inventory on screen
        inventory_x = (screen_width - inventory_width) // 2
        inventory_y = (screen_height - inventory_height) // 2
        
        # Draw semi-transparent background
        inventory_surface = pygame.Surface((inventory_width, inventory_height), pygame.SRCALPHA)
        inventory_surface.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(inventory_surface, (inventory_x, inventory_y))
        
        # Draw inventory border
        pygame.draw.rect(screen, (255, 255, 255), 
                        (inventory_x, inventory_y, inventory_width, inventory_height), 2)
        
        # Draw title
        font_title = pygame.font.Font(None, 36)
        title_text = font_title.render("Inventory", True, (255, 255, 255))
        screen.blit(title_text, (inventory_x + 10, inventory_y - 36))
        
        # Draw slots
        for i in range(self.size):
            row = i // self.slots_per_row
            col = i % self.slots_per_row
            
            slot_x = inventory_x + self.slot_padding + col * (self.slot_size + self.slot_padding)
            slot_y = inventory_y + self.slot_padding + row * (self.slot_size + self.slot_padding)
            
            # Draw slot background
            slot_color = (50, 50, 50) if i != self.selected_index else (70, 70, 100)
            pygame.draw.rect(screen, slot_color, (slot_x, slot_y, self.slot_size, self.slot_size))
            pygame.draw.rect(screen, (100, 100, 100), (slot_x, slot_y, self.slot_size, self.slot_size), 1)
            
            # Draw item if slot has one
            if i < len(self.items):
                item = self.items[i]
                screen.blit(item.icon, (slot_x + 4, slot_y + 4))
                
                # Draw stack count if stackable
                if item.stackable and item.count > 1:
                    font_count = pygame.font.Font(None, 20)
                    count_text = font_count.render(str(item.count), True, (255, 255, 255))
                    screen.blit(count_text, (slot_x + self.slot_size - 10, slot_y + self.slot_size - 15))
                
                # Highlight equipped items
                if hasattr(item, 'equipped') and item.equipped:
                    pygame.draw.rect(screen, (0, 255, 0), (slot_x, slot_y, self.slot_size, self.slot_size), 2)
                
                # Show tooltip for selected item
                if i == self.selected_index and self.show_tooltip:
                    self._draw_tooltip(screen, item, slot_x, slot_y)
    
    def _draw_tooltip(self, screen, item, slot_x, slot_y):
        """Draw tooltip for the item"""
        font = pygame.font.Font(None, 20)
        name_text = font.render(item.name, True, (255, 255, 255))
        desc_lines = self._wrap_text(item.description, 200, font)
        
        # Calculate tooltip dimensions
        tooltip_width = max(name_text.get_width(), max([font.size(line)[0] for line in desc_lines])) + 20
        tooltip_height = 10 + len(desc_lines) * font.get_linesize() + 30
        
        # Position tooltip
        tooltip_x = slot_x + self.slot_size + 5
        tooltip_y = slot_y
        
        # Make sure tooltip stays on screen
        if tooltip_x + tooltip_width > screen.get_width():
            tooltip_x = slot_x - tooltip_width - 5
        if tooltip_y + tooltip_height > screen.get_height():
            tooltip_y = screen.get_height() - tooltip_height
        
        # Draw tooltip background
        pygame.draw.rect(screen, (30, 30, 30, 220), 
                        (tooltip_x, tooltip_y, tooltip_width, tooltip_height))
        pygame.draw.rect(screen, (200, 200, 200), 
                        (tooltip_x, tooltip_y, tooltip_width, tooltip_height), 1)
        
        # Draw item name
        screen.blit(name_text, (tooltip_x + 10, tooltip_y + 10))
        
        # Draw description
        for i, line in enumerate(desc_lines):
            line_surf = font.render(line, True, (200, 200, 200))
            screen.blit(line_surf, (tooltip_x + 10, tooltip_y + 30 + i * font.get_linesize()))
    
    def _wrap_text(self, text, max_width, font):
        """Wrap text to fit within a certain width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
