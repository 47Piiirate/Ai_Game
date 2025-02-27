import pygame
import os

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.music_tracks = {}
        self.load_assets()

    def load_assets(self):
        """Load all game assets"""
        self.load_images()
        self.load_sounds()
        self.load_music()

    def load_images(self):
        """Load images from the assets/images directory"""
        image_files = [
            "Sprites/Characters/Heros/Main Hero/hero_complete_sheet.png",
            "Sprites/Characters/Heros/Main Hero/Idle-Sheet.png",
            "Sprites/Characters/Heros/Main Hero/Run-Sheet.png",
            "Sprites/Characters/Enemies/Bipedo Creature/bipedo_full_sheet.png",
            "Sprites/Characters/Enemies/Fly Creature/flying_creature_complete_sheet.png",
            "Sprites/Characters/Enemies/Slime/silme_complete_sheet.png",
            "Sprites/HUD/Selector_Projectile_HUD.png",
            "Sprites/HUD/Boss Bar/boss_bar_1_full.png",
            "Sprites/HUD/Health Bar/Health_Bar_HUD.png",
            "Sprites/Tileset/Tileset.png",
            "Sprites/VFX/Explosion-Sheet.png",
            # Add more images as needed
        ]

        for image_file in image_files:
            try:
                image_path = os.path.join("assets", image_file)
                image = pygame.image.load(image_path).convert_alpha()
                self.images[image_file] = image
                print(f"Loaded image: {image_file}")  # Log successful loading
            except Exception as e:
                print(f"Warning: Could not load image {image_file}: {e}")

    def load_sounds(self):
        """Load sound effects from the assets/sounds directory"""
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
        
        for sound_name, file_path in sound_files.items():
            try:
                # Skip loading sound if the file does not exist
                sound_path = os.path.join("assets", "sounds", file_path)
                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)
                    self.sounds[sound_name] = sound
                else:
                    print(f"Warning: Sound file does not exist, skipping {file_path}")
            except Exception as e:
                print(f"Warning: Could not load sound {file_path}: {e}")

    def load_music(self):
        """Load music tracks from the assets/music directory"""
        music_files = {
            "title": "title_theme.mp3",
            "main_area": "main_area.mp3",
            "cave": "cave.mp3",
            "boss": "boss.mp3",
            "victory": "victory.mp3",
            "game_over": "game_over.mp3"
        }
        
        for music_name, file_path in music_files.items():
            self.music_tracks[music_name] = os.path.join("assets", "music", file_path)

    def get_image(self, image_name):
        """Get an image by name"""
        return self.images.get(image_name)

    def get_sound(self, sound_name):
        """Get a sound by name"""
        return self.sounds.get(sound_name)

    def get_music(self, music_name):
        """Get a music track by name"""
        return self.music_tracks.get(music_name)

def load_image(file_path):
    try:
        image = pygame.image.load(file_path)
        print(f"Loaded image: {file_path}")
        return image
    except pygame.error as e:
        print(f"Error loading image {file_path}: {e}")
        return None

def load_assets():
    assets = {
        "hero_complete_sheet": load_image("Sprites/Characters/Heros/Main Hero/hero_complete_sheet.png"),
        "idle_sheet": load_image("Sprites/Characters/Heros/Main Hero/Idle-Sheet.png"),
        "run_sheet": load_image("Sprites/Characters/Heros/Main Hero/Run-Sheet.png"),
        "bipedo_full_sheet": load_image("Sprites/Characters/Enemies/Bipedo Creature/bipedo_full_sheet.png"),
        "flying_creature_complete_sheet": load_image("Sprites/Characters/Enemies/Fly Creature/flying_creature_complete_sheet.png"),
        "silme_complete_sheet": load_image("Sprites/Characters/Enemies/Slime/silme_complete_sheet.png"),
        "selector_projectile_hud": load_image("Sprites/HUD/Selector_Projectile_HUD.png"),
        "boss_bar_1_full": load_image("Sprites/HUD/Boss Bar/boss_bar_1_full.png"),
        "health_bar_hud": load_image("Sprites/HUD/Health Bar/Health_Bar_HUD.png"),
        "tileset": load_image("Sprites/Tileset/Tileset.png"),
        "explosion_sheet": load_image("Sprites/VFX/Explosion-Sheet.png")
    }
    return assets

# Example usage
if __name__ == "__main__":
    pygame.init()
    asset_manager = AssetManager()
    # Now you can use asset_manager to access images, sounds, and music
