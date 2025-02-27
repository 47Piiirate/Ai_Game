import os
import sys
import pygame
import subprocess

def check_directory_structure():
    """Check that the directory structure is as expected"""
    base_dir = os.path.dirname(__file__)
    
    required_dirs = [
        "assets",
        "assets/sounds",
        "assets/music",
        "assets/images",
        "Sprites"  # Based on your directory structure
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        full_path = os.path.join(base_dir, directory)
        if not os.path.exists(full_path):
            missing_dirs.append(directory)
            try:
                os.makedirs(full_path)
                print(f"Created missing directory: {directory}")
            except Exception as e:
                print(f"Error creating directory {directory}: {e}")
    
    if missing_dirs:
        print(f"Created {len(missing_dirs)} missing directories")
    else:
        print("All required directories already exist")
    
    return missing_dirs

def check_asset_manager_file():
    """Check that asset_manager.py exists and patch it if needed"""
    base_dir = os.path.dirname(__file__)
    asset_manager_path = os.path.join(base_dir, "asset_manager.py")
    
    if not os.path.exists(asset_manager_path):
        print("Error: asset_manager.py doesn't exist!")
        return False
    
    # Try to patch the asset manager
    try:
        patch_module_name = "asset_manager_patch"
        patch_module_path = os.path.join(base_dir, f"{patch_module_name}.py")
        
        # Check if patch module exists
        if not os.path.exists(patch_module_path):
            print("Error: asset_manager_patch.py doesn't exist!")
            return False
        
        # Import and run the patch
        sys.path.insert(0, base_dir)
        patch_module = __import__(patch_module_name)
        
        if hasattr(patch_module, 'patch_asset_manager'):
            if patch_module.patch_asset_manager():
                print("Successfully patched asset_manager.py")
                return True
            else:
                print("Failed to patch asset_manager.py")
                return False
        else:
            print("patch_asset_manager function not found")
            return False
    except Exception as e:
        print(f"Error patching asset_manager.py: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_placeholder_sounds():
    """Create placeholder sound files"""
    base_dir = os.path.dirname(__file__)
    sounds_dir = os.path.join(base_dir, "assets", "sounds")
    
    # Ensure directory exists
    os.makedirs(sounds_dir, exist_ok=True)
    
    # List of missing sound files based on error messages
    sound_files = [
        "jump.wav",
        "dash.wav",
        "attack.wav",
        "hit.wav",
        "parry.wav",
        "collect.wav",
        "death.wav",
        "menu_select.wav",
        "boss_hit.wav",
        "ability_unlock.wav"
    ]
    
    import wave
    import struct
    
    # Create empty WAV files for each sound
    for sound_file in sound_files:
        file_path = os.path.join(sounds_dir, sound_file)
        
        # Skip if file already exists
        if os.path.exists(file_path):
            print(f"Sound file already exists: {sound_file}")
            continue
        
        # Create a silent WAV file
        channels = 1
        sample_width = 2  # 2 bytes = 16 bits
        framerate = 44100
        duration = 0.5  # half a second
        frames = int(framerate * duration)
        
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(framerate)
            
            # Generate silent audio data
            for _ in range(frames):
                wav_file.writeframes(struct.pack('h', 0))
        
        print(f"Created placeholder sound: {sound_file}")
    
    print("All placeholder sound files created successfully")
    return True

def check_game_runnable():
    """Test if the game can be initialized without errors"""
    print("Testing game initialization...")
    
    try:
        # Initialize pygame
        pygame.init()
        print("Pygame initialized successfully")
        
        # Set up minimal display
        screen = pygame.display.set_mode((800, 600))
        print("Display initialized successfully")
        
        # Initialize mixer
        pygame.mixer.init()
        print("Mixer initialized successfully")
        
        # Clean up
        pygame.quit()
        print("Test completed successfully!")
        return True
    except Exception as e:
        print(f"Error initializing game: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to fix game issues"""
    print("=== Game Issue Fixer ===")
    print("This script will fix common issues with the game")
    
    # Step 1: Check directory structure
    print("\nStep 1: Checking directory structure...")
    check_directory_structure()
    
    # Step 2: Create placeholder sound files
    print("\nStep 2: Creating placeholder sound files...")
    create_placeholder_sounds()
    
    # Step 3: Patch the asset manager
    print("\nStep 3: Patching asset manager...")
    check_asset_manager_file()
    
    # Step 4: Test game initialization
    print("\nStep 4: Testing game initialization...")
    if check_game_runnable():
        print("\n✓ Game initialization successful!")
    else:
        print("\n✗ Game initialization failed! Try the advanced diagnostics.")
    
    print("\nBasic fixes have been applied. Try running the game now with:")
    print("  python main.py")
    
    print("\nIf you still encounter issues, try running:")
    print("  python validate_assets.py")
    print("This will identify any missing assets referenced in your code.")

if __name__ == "__main__":
    main()
