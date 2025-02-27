import pygame
import os

class SoundManager:
    def __init__(self):
        # Initialize sound mixer
        pygame.mixer.init()
        
        # Sound effects dictionary
        self.sounds = {}
        
        # Music tracks dictionary
        self.music_tracks = {}
        
        # Missing music tracks to avoid repeated warnings
        self.missing_tracks = set()
        
        # Volume settings
        self.sfx_volume = 0.7
        self.music_volume = 0.5
        
        # Current music track
        self.current_music = None
        
        # Load sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects and music tracks"""
        # Sound effects paths (these would be actual files in a real game)
        sound_files = {
            "jump": "jump.wav",
            "dash": "dash.wav",
            "attack": "attack.wav",
            "hit": "hit.wav",
            "parry": "parry.wav",
            "collect": "collect.wav",
            "death": "death.wav",
            "menu_select": "menu_select.wav",
            "boss_hit": "boss_hit.wav",
            "ability_unlock": "ability_unlock.wav"
        }
        
        # Music track paths
        music_files = {
            "title": "title_theme.mp3",
            "main_area": "main_area.mp3",
            "cave": "cave.mp3",
            "boss": "boss.mp3",
            "victory": "victory.mp3",
            "game_over": "game_over.mp3"
        }
        
        # Load sound effects (with error handling if files don't exist)
        for sound_name, file_path in sound_files.items():
            try:
                sound = pygame.mixer.Sound(os.path.join("assets", "sounds", file_path))
                sound.set_volume(self.sfx_volume)
                self.sounds[sound_name] = sound
            except:
                print(f"Warning: Could not load sound {file_path}")
        
        # Store music file paths (we'll load them when needed)
        for music_name, file_path in music_files.items():
            self.music_tracks[music_name] = os.path.join("assets", "music", file_path)
    
    def play_sound(self, sound_name):
        """Play a sound effect by name"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, music_name, loop=True):
        """Start playing a music track by name"""
        if self.current_music == music_name:
            return  # Already playing this track
        
        # Skip if we already know this track is missing
        if music_name in self.missing_tracks:
            return
            
        if music_name in self.music_tracks:
            try:
                filepath = self.music_tracks[music_name]
                
                # Check if file actually exists before trying to play
                if not os.path.exists(filepath):
                    print(f"Warning: Music file does not exist: {filepath}")
                    self.missing_tracks.add(music_name)  # Remember it's missing
                    return
                
                pygame.mixer.music.stop()
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music = music_name
            except Exception as e:
                print(f"Warning: Could not play music {music_name}: {e}")
                self.missing_tracks.add(music_name)  # Remember it's missing
    
    def stop_music(self):
        """Stop the current music track"""
        pygame.mixer.music.stop()
        self.current_music = None
    
    def pause_music(self):
        """Pause the current music track"""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Resume the paused music track"""
        pygame.mixer.music.unpause()
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
