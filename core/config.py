"""
Game configuration settings
"""
import os
import json

class Config:
    """
    Manages game configuration settings
    """
    # Default configuration values
    DEFAULT_CONFIG = {
        "video": {
            "width": 800,
            "height": 600,
            "fullscreen": False,
            "vsync": True,
            "fps_limit": 60
        },
        "audio": {
            "music_volume": 0.7,
            "sfx_volume": 0.8,
            "mute": False
        },
        "controls": {
            "keyboard": {
                "left": "LEFT",
                "right": "RIGHT",
                "up": "UP",
                "down": "DOWN",
                "jump": "SPACE",
                "attack": "z",
                "special": "x",
                "pause": "ESCAPE"
            },
            "gamepad": True
        },
        "gameplay": {
            "difficulty": "normal",
            "show_fps": False,
            "show_hitboxes": False
        },
        "development": {
            "debug_mode": False,
            "log_level": "INFO"
        }
    }
    
    def __init__(self, config_path="config.json"):
        """Initialize the configuration"""
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    
                    # Merge loaded config with defaults (to ensure all keys exist)
                    self._merge_configs(self.config, loaded_config)
                    
                print(f"Configuration loaded from {self.config_path}")
            else:
                print(f"No configuration file found at {self.config_path}, using defaults")
                self.save()  # Create a default config file
        except Exception as e:
            print(f"Error loading configuration: {e}")
            print("Using default configuration")
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def _merge_configs(self, target, source):
        """
        Recursively merge source config into target config
        Only values for existing keys will be updated
        """
        for key, value in source.items():
            if key in target:
                if isinstance(value, dict) and isinstance(target[key], dict):
                    self._merge_configs(target[key], value)
                else:
                    target[key] = value
    
    def get(self, section, key=None, default=None):
        """
        Get a configuration value
        
        Args:
            section: Configuration section
            key: Configuration key within section (None for entire section)
            default: Default value if key doesn't exist
        """
        if section not in self.config:
            return default
            
        if key is None:
            return self.config[section]
            
        if key not in self.config[section]:
            return default
            
        return self.config[section][key]
    
    def set(self, section, key, value):
        """
        Set a configuration value
        
        Args:
            section: Configuration section
            key: Configuration key within section
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section][key] = value
    
    def update_video_settings(self, width=None, height=None, fullscreen=None, vsync=None, fps_limit=None):
        """Update video settings"""
        if width is not None:
            self.config["video"]["width"] = width
        if height is not None:
            self.config["video"]["height"] = height
        if fullscreen is not None:
            self.config["video"]["fullscreen"] = fullscreen
        if vsync is not None:
            self.config["video"]["vsync"] = vsync
        if fps_limit is not None:
            self.config["video"]["fps_limit"] = fps_limit
            
        # Save the updated configuration
        self.save()
