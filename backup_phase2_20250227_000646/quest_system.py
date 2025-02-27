import pygame
import json
import os
from enum import Enum, auto

class QuestStatus(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()

class QuestObjective:
    """Represents a single objective within a quest"""
    def __init__(self, description, required_amount=1, current_amount=0, completed=False):
        self.description = description
        self.required_amount = required_amount
        self.current_amount = current_amount
        self.completed = completed
    
    def update(self, amount=1):
        """Update progress towards this objective"""
        if self.completed:
            return False
        
        self.current_amount += amount
        if self.current_amount >= self.required_amount:
            self.current_amount = self.required_amount
            self.completed = True
            return True  # Indicates completion
        
        return False
    
    def get_progress_percentage(self):
        """Get completion percentage for this objective"""
        return (self.current_amount / self.required_amount) * 100 if self.required_amount > 0 else 0
    
    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            "description": self.description,
            "required_amount": self.required_amount,
            "current_amount": self.current_amount,
            "completed": self.completed
        }
    
    @staticmethod
    def from_dict(data):
        """Create objective from dictionary"""
        return QuestObjective(
            data["description"],
            data.get("required_amount", 1),
            data.get("current_amount", 0),
            data.get("completed", False)
        )

class Quest:
    """Represents a quest with objectives and rewards"""
    def __init__(self, quest_id, title, description):
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.objectives = []
        self.rewards = {}  # Dict of reward types and values
        self.status = QuestStatus.NOT_STARTED
        self.giver_npc = None
        self.completion_npc = None
        self.prerequisites = []  # List of quest IDs that must be completed first
        self.hidden = False  # If True, won't show in quest log until discovered
    
    def add_objective(self, description, required_amount=1):
        """Add an objective to this quest"""
        self.objectives.append(QuestObjective(description, required_amount))
    
    def add_reward(self, reward_type, value):
        """Add a reward for completing this quest"""
        self.rewards[reward_type] = value
    
    def is_complete(self):
        """Check if all objectives are completed"""
        return all(objective.completed for objective in self.objectives)
    
    def update_objective(self, index, amount=1):
        """Update progress for a specific objective by index"""
        if 0 <= index < len(self.objectives):
            return self.objectives[index].update(amount)
        return False
    
    def update_objective_by_description(self, description, amount=1):
        """Update progress for a specific objective by description"""
        for objective in self.objectives:
            if objective.description == description:
                return objective.update(amount)
        return False
    
    def update_status(self):
        """Update the quest status based on objectives"""
        if self.status == QuestStatus.COMPLETED or self.status == QuestStatus.FAILED:
            return self.status
        
        if self.status == QuestStatus.NOT_STARTED:
            self.status = QuestStatus.IN_PROGRESS
        
        if self.is_complete():
            self.status = QuestStatus.COMPLETED
        
        return self.status
    
    def get_completion_percentage(self):
        """Get the overall completion percentage for this quest"""
        if not self.objectives:
            return 0
        
        total = sum(obj.get_progress_percentage() for obj in self.objectives)
        return total / len(self.objectives)
    
    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            "id": self.quest_id,
            "status": self.status.name,
            "objectives": [obj.to_dict() for obj in self.objectives]
        }
    
    @staticmethod
    def from_dict(data, quest_database):
        """Create quest from dictionary and base quest data"""
        if data["id"] in quest_database:
            # Get base quest template
            base_quest = quest_database[data["id"]]
            
            # Create a new quest instance
            quest = Quest(base_quest.quest_id, base_quest.title, base_quest.description)
            quest.giver_npc = base_quest.giver_npc
            quest.completion_npc = base_quest.completion_npc
            quest.prerequisites = base_quest.prerequisites
            quest.rewards = base_quest.rewards.copy()
            quest.hidden = base_quest.hidden
            
            # Set status
            quest.status = QuestStatus[data["status"]]
            
            # Set objectives
            if "objectives" in data:
                for i, obj_data in enumerate(data["objectives"]):
                    if i < len(base_quest.objectives):
                        # Update existing objective with saved progress
                        quest.objectives.append(QuestObjective.from_dict(obj_data))
                    else:
                        # If there are extra objectives in the save, add them
                        quest.objectives.append(QuestObjective.from_dict(obj_data))
            else:
                # Use default objectives
                quest.objectives = [QuestObjective(obj.description, obj.required_amount) 
                                  for obj in base_quest.objectives]
            
            return quest
        
        return None

class QuestManager:
    """Manages all quests in the game"""
    def __init__(self):
        self.quests = {}  # All available quests by ID
        self.active_quests = {}  # Currently active quests
        self.completed_quests = {}  # Completed quests
        self.quest_log_visible = False
        self.selected_quest_index = 0
        self.quest_database = {}  # Database of quest templates
        
        # Load quest templates
        self._load_quest_database()
    
    def _load_quest_database(self):
        """Load quest definitions from file"""
        quests_dir = os.path.join("assets", "quests")
        os.makedirs(quests_dir, exist_ok=True)
        
        quest_file = os.path.join(quests_dir, "quests.json")
        if os.path.exists(quest_file):
            try:
                with open(quest_file, "r") as f:
                    quest_data = json.load(f)
                
                # Create quest templates from data
                for quest_info in quest_data:
                    quest = Quest(
                        quest_info["id"],
                        quest_info["title"],
                        quest_info["description"]
                    )
                    
                    # Add objectives
                    for obj_info in quest_info.get("objectives", []):
                        quest.add_objective(
                            obj_info["description"],
                            obj_info.get("required_amount", 1)
                        )
                    
                    # Add rewards
                    for reward_type, value in quest_info.get("rewards", {}).items():
                        quest.add_reward(reward_type, value)
                    
                    # Set other properties
                    quest.giver_npc = quest_info.get("giver_npc")
                    quest.completion_npc = quest_info.get("completion_npc")
                    quest.prerequisites = quest_info.get("prerequisites", [])
                    quest.hidden = quest_info.get("hidden", False)
                    
                    self.quest_database[quest.quest_id] = quest
                
                print(f"Loaded {len(self.quest_database)} quests from database")
            except Exception as e:
                print(f"Error loading quest database: {e}")
    
    def get_available_quests(self):
        """Get quests that can be started based on prerequisites"""
        available = []
        
        for quest_id, quest in self.quest_database.items():
            # Skip if already active or completed
            if quest_id in self.active_quests or quest_id in self.completed_quests:
                continue
            
            # Check prerequisites
            prereqs_met = True
            for prereq_id in quest.prerequisites:
                if prereq_id not in self.completed_quests:
                    prereqs_met = False
                    break
            
            if prereqs_met and not quest.hidden:
                available.append(quest)
        
        return available
    
    def start_quest(self, quest_id):
        """Start a quest by ID"""
        if quest_id not in self.quest_database:
            print(f"Quest ID {quest_id} not found in database")
            return False
        
        if quest_id in self.active_quests:
            print(f"Quest {quest_id} already active")
            return False
        
        if quest_id in self.completed_quests:
            print(f"Quest {quest_id} already completed")
            return False
        
        # Check prerequisites
        quest = self.quest_database[quest_id]
        for prereq_id in quest.prerequisites:
            if prereq_id not in self.completed_quests:
                print(f"Prerequisite quest {prereq_id} not completed")
                return False
        
        # Create a new instance of the quest
        new_quest = Quest(quest.quest_id, quest.title, quest.description)
        new_quest.giver_npc = quest.giver_npc
        new_quest.completion_npc = quest.completion_npc
        new_quest.rewards = quest.rewards.copy()
        new_quest.prerequisites = quest.prerequisites.copy()
        new_quest.hidden = quest.hidden
        
        # Add objectives
        for obj in quest.objectives:
            new_quest.add_objective(obj.description, obj.required_amount)
        
        # Activate the quest
        new_quest.status = QuestStatus.IN_PROGRESS
        self.active_quests[quest_id] = new_quest
        
        print(f"Started quest: {new_quest.title}")
        return True
    
    def update_quest(self, quest_id, objective_description, amount=1):
        """Update progress for a specific quest objective"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            updated = quest.update_objective_by_description(objective_description, amount)
            
            if updated:
                quest.update_status()
                
                # Check if quest is completed
                if quest.status == QuestStatus.COMPLETED:
                    print(f"Quest completed: {quest.title}")
                    
                return updated
        
        return False
    
    def complete_quest(self, quest_id):
        """Mark a quest as completed and give rewards"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            
            # Ensure all objectives are complete
            if not quest.is_complete():
                for obj in quest.objectives:
                    obj.current_amount = obj.required_amount
                    obj.completed = True
            
            quest.status = QuestStatus.COMPLETED
            
            # Move to completed quests
            self.completed_quests[quest_id] = quest
            del self.active_quests[quest_id]
            
            # Return rewards
            return quest.rewards
        
        return {}
    
    def fail_quest(self, quest_id):
        """Mark a quest as failed"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            quest.status = QuestStatus.FAILED
            
            # Remove from active quests
            del self.active_quests[quest_id]
            
            return True
        
        return False
    
    def toggle_quest_log(self):
        """Toggle visibility of quest log"""
        self.quest_log_visible = not self.quest_log_visible
    
    def render_quest_log(self, screen):
        """Render the quest log UI"""
        if not self.quest_log_visible:
            return
        
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Create semi-transparent background
        log_width = 600
        log_height = 400
        log_x = (screen_width - log_width) // 2
        log_y = (screen_height - log_height) // 2
        
        # Draw background
        log_surface = pygame.Surface((log_width, log_height), pygame.SRCALPHA)
        log_surface.fill((0, 0, 0, 220))  # Semi-transparent black
        screen.blit(log_surface, (log_x, log_y))
        
        # Draw border
        pygame.draw.rect(screen, (200, 200, 200), (log_x, log_y, log_width, log_height), 2)
        
        # Draw title
        font_title = pygame.font.Font(None, 36)
        title_text = font_title.render("Quest Log", True, (255, 255, 255))
        screen.blit(title_text, (log_x + 20, log_y + 20))
        
        # Draw active quests
        if not self.active_quests:
            no_quests_text = pygame.font.Font(None, 24).render(
                "No active quests", True, (200, 200, 200))
            screen.blit(no_quests_text, (log_x + 20, log_y + 70))
        else:
            # Create list of quests
            quests = list(self.active_quests.values())
            
            # Draw quest list
            font_quest = pygame.font.Font(None, 24)
            font_desc = pygame.font.Font(None, 18)
            
            list_width = 200
            detail_x = log_x + list_width + 20
            
            # Draw quest list on left side
            for i, quest in enumerate(quests):
                # Highlight selected quest
                color = (255, 255, 0) if i == self.selected_quest_index else (255, 255, 255)
                quest_text = font_quest.render(f"{i+1}. {quest.title}", True, color)
                
                # Draw completion percentage
                progress = quest.get_completion_percentage()
                progress_text = font_desc.render(f"{progress:.0f}%", True, color)
                
                # Position text
                quest_y = log_y + 70 + i * 25
                screen.blit(quest_text, (log_x + 20, quest_y))
                screen.blit(progress_text, (log_x + list_width - 40, quest_y))
            
            # Draw details of selected quest on right side
            if 0 <= self.selected_quest_index < len(quests):
                selected_quest = quests[self.selected_quest_index]
                
                # Quest title
                title_text = font_quest.render(selected_quest.title, True, (255, 255, 0))
                screen.blit(title_text, (detail_x, log_y + 70))
                
                # Quest description
                desc_lines = self._wrap_text(selected_quest.description, 300, font_desc)
                for i, line in enumerate(desc_lines):
                    desc_text = font_desc.render(line, True, (200, 200, 200))
                    screen.blit(desc_text, (detail_x, log_y + 100 + i * font_desc.get_linesize()))
                
                # Quest objectives
                obj_y = log_y + 140 + len(desc_lines) * font_desc.get_linesize()
                screen.blit(font_quest.render("Objectives:", True, (255, 255, 255)), 
                          (detail_x, obj_y))
                
                for i, objective in enumerate(selected_quest.objectives):
                    # Create checkmark or empty box based on completion
                    check_char = "✓" if objective.completed else "□"
                    check_color = (0, 255, 0) if objective.completed else (200, 200, 200)
                    
                    # Create objective text
                    obj_text = f"{objective.description}"
                    if objective.required_amount > 1:
                        obj_text += f" ({objective.current_amount}/{objective.required_amount})"
                    
                    # Draw checkbox and text
                    check_surf = font_quest.render(check_char, True, check_color)
                    obj_surf = font_desc.render(obj_text, True, (255, 255, 255))
                    
                    obj_line_y = obj_y + 30 + i * 25
                    screen.blit(check_surf, (detail_x, obj_line_y))
                    screen.blit(obj_surf, (detail_x + 20, obj_line_y))
    
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
    
    def save_quest_progress(self):
        """Save quest progress to file"""
        save_data = {
            "active_quests": {quest_id: quest.to_dict() for quest_id, quest in self.active_quests.items()},
            "completed_quests": {quest_id: quest.to_dict() for quest_id, quest in self.completed_quests.items()}
        }
        
        save_dir = os.path.join("saves", "quests")
        os.makedirs(save_dir, exist_ok=True)
        
        try:
            with open(os.path.join(save_dir, "quests.json"), "w") as f:
                json.dump(save_data, f, indent=2)
            print("Quest progress saved successfully")
            return True
        except Exception as e:
            print(f"Error saving quest progress: {e}")
            return False
    
    def load_quest_progress(self):
        """Load quest progress from file"""
        save_dir = os.path.join("saves", "quests")
        save_file = os.path.join(save_dir, "quests.json")
        
        if not os.path.exists(save_file):
            print("No quest save file found")
            return False
        
        try:
            with open(save_file, "r") as f:
                save_data = json.load(f)
            
            # Clear existing quest data
            self.active_quests = {}
            self.completed_quests = {}
            
            # Load active quests
            for quest_id, quest_data in save_data.get("active_quests", {}).items():
                quest = Quest.from_dict(quest_data, self.quest_database)
                if quest:
                    self.active_quests[quest_id] = quest
            
            # Load completed quests
            for quest_id, quest_data in save_data.get("completed_quests", {}).items():
                quest = Quest.from_dict(quest_data, self.quest_database)
                if quest:
                    self.completed_quests[quest_id] = quest
            
            print(f"Loaded {len(self.active_quests)} active and {len(self.completed_quests)} completed quests")
            return True
        except Exception as e:
            print(f"Error loading quest progress: {e}")
            return False
    
    def handle_input(self, event):
        """Handle input for quest log"""
        if not self.quest_log_visible:
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Move selection up
                if self.active_quests:
                    self.selected_quest_index = (self.selected_quest_index - 1) % len(self.active_quests)
            elif event.key == pygame.K_DOWN:
                # Move selection down
                if self.active_quests:
                    self.selected_quest_index = (self.selected_quest_index + 1) % len(self.active_quests)
            elif event.key == pygame.K_ESCAPE:
                # Close quest log
                self.quest_log_visible = False