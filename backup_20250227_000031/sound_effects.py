import pygame
import math
import os

class SoundEffectManager:
    """Manages sound effects with features like positional audio and pooling"""
    def __init__(self):
        # Sound pools (to avoid creating too many sound channels)
        self.sound_pools = {}
        self.pool_sizes = {
            "common": 8,  # Common sounds like footsteps
            "rare": 4,    # Less common sounds
            "unique": 2,  # Sounds that rarely overlap
        }
        
        # Default settings
        self.master_volume = 0.7
        self.effects_volume = 1.0
        self.max_distance = 1000  # Max distance for positional audio
        self.reference_distance = 300  # Distance at which volume starts to decrease
        self.position_enabled = True
        
        # Camera and screen properties for positional audio
        self.camera_x = 0
        self.camera_y = 0
        self.screen_width = 800
        self.screen_height = 600
        
        # Initialize sound pools
        self._init_pools()
    
    def _init_pools(self):
        """Initialize sound pools"""
        for pool_name, size in self.pool_sizes.items():
            self.sound_pools[pool_name] = [None] * size
    
    def load_sound(self, name, file_path, pool="common"):
        """Load a sound and add it to the appropriate pool"""
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(self.effects_volume * self.master_volume)
            
            # Create pool entry
            self.sound_pools[pool].append({
                "name": name,
                "sound": sound,
                "playing": False,
                "channel": None,
                "position": None,
                "last_played": 0
            })
            
            return True
        except Exception as e:
            print(f"Error loading sound {name}: {e}")
            return False
    
    def load_sound_directory(self, directory):
        """Load all sounds from a directory"""
        loaded = 0
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith((".wav", ".ogg", ".mp3")):
                    name = os.path.splitext(file)[0]
                    path = os.path.join(root, file)
                    
                    # Determine pool based on naming convention or subdirectory
                    if "footstep" in name.lower() or "ambient" in name.lower():
                        pool = "common"
                    elif "attack" in name.lower() or "hit" in name.lower():
                        pool = "rare"
                    else:
                        pool = "unique"
                    
                    if self.load_sound(name, path, pool):
                        loaded += 1
        
        print(f"Loaded {loaded} sound effects")
        return loaded
    
    def play(self, name, volume=1.0, position=None):
        """Play a sound with optional positional audio"""
        # Find the sound in pools
        sound_entry = None
        pool_name = None
        
        for p_name, pool in self.sound_pools.items():
            for entry in pool:
                if entry is not None and entry["name"] == name:
                    sound_entry = entry
                    pool_name = p_name
                    break
            if sound_entry:
                break
        
        if not sound_entry:
            print(f"Sound '{name}' not found")
            return False
        
        # Calculate volume based on position if enabled
        if position and self.position_enabled:
            listener_pos = (self.camera_x + self.screen_width / 2, 
                           self.camera_y + self.screen_height / 2)
            
            # Calculate distance from listener to sound
            dx = position[0] - listener_pos[0]
            dy = position[1] - listener_pos[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Linear falloff
            if distance >= self.max_distance:
                volume = 0.0
            elif distance > self.reference_distance:
                volume *= 1.0 - ((distance - self.reference_distance) / 
                                (self.max_distance - self.reference_distance))
        
        # Find an available channel in the pool
        available_channel = None
        for i, entry in enumerate(self.sound_pools[pool_name]):
            if entry is None or not entry["playing"]:
                available_channel = i
                break
        
        # If no channels available, find the oldest one
        if available_channel is None:
            oldest_time = pygame.time.get_ticks()
            oldest_index = 0
            for i, entry in enumerate(self.sound_pools[pool_name]):
                if entry["last_played"] < oldest_time:
                    oldest_time = entry["last_played"]
                    oldest_index = i
            available_channel = oldest_index
        
        # Play the sound
        sound_entry["sound"].set_volume(volume * self.effects_volume * self.master_volume)
        channel = sound_entry["sound"].play()
        
        # Update entry
        sound_entry["playing"] = True
        sound_entry["channel"] = channel
        sound_entry["position"] = position
        sound_entry["last_played"] = pygame.time.get_ticks()
        
        return True
    
    def stop(self, name=None):
        """Stop a specific sound or all sounds"""
        if name:
            # Stop only the specified sound
            for pool in self.sound_pools.values():
                for entry in pool:
                    if entry is not None and entry["name"] == name and entry["playing"]:
                        if entry["channel"]:
                            entry["channel"].stop()
                        entry["playing"] = False
        else:
            # Stop all sounds
            for pool in self.sound_pools.values():
                for entry in pool:
                    if entry is not None and entry["playing"]:
                        if entry["channel"]:
                            entry["channel"].stop()
                        entry["playing"] = False
    
    def set_master_volume(self, volume):
        """Set master volume for all sounds"""
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()
    
    def set_effects_volume(self, volume):
        """Set effects volume"""
        self.effects_volume = max(0.0, min(1.0, volume))
        self._update_volumes()
    
    def _update_volumes(self):
        """Update volumes for all sounds"""
        for pool in self.sound_pools.values():
            for entry in pool:
                if entry is not None:
                    entry["sound"].set_volume(self.effects_volume * self.master_volume)
    
    def update_camera(self, camera_x, camera_y):
        """Update camera position for positional audio"""
        self.camera_x = camera_x
        self.camera_y = camera_y
    
    def set_screen_size(self, width, height):
        """Set screen size for positional audio calculations"""
        self.screen_width = width
        self.screen_height = height