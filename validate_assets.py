import os
import sys
import pygame
from pprint import pprint
import json

def scan_for_assets():
    """Scan through game files to detect referenced assets"""
    project_dir = os.path.dirname(__file__)
    
    # Patterns to look for in code files
    asset_patterns = [
        'load_image', 'load_sound', 'play_sound', 'play_music',
        'pygame.image.load', 'pygame.mixer.Sound', 'pygame.mixer.music.load'
    ]
    
    # Store found asset references
    found_assets = {
        'images': set(),
        'sounds': set(),
        'music': set(),
        'other': set()
    }
    
    # Extensions to check for code files
    code_extensions = ['.py']
    
    # Scan through all python files for asset references
    print("Scanning for asset references in code...")
    for root, _, files in os.walk(project_dir):
        for file in files:
            if any(file.endswith(ext) for ext in code_extensions):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Look for asset patterns
                        for pattern in asset_patterns:
                            if pattern in content:
                                # Extract possible filenames after the pattern
                                import re
                                matches = re.findall(fr'{pattern}\([\'"]([^\'"]+)[\'"]', content)
                                
                                for match in matches:
                                    if match.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                                        found_assets['images'].add(match)
                                    elif match.lower().endswith('.wav'):
                                        found_assets['sounds'].add(match)
                                    elif match.lower().endswith(('.mp3', '.ogg')):
                                        found_assets['music'].add(match)
                                    else:
                                        found_assets['other'].add(match)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    
    return found_assets

def verify_assets_exist(found_assets):
    """Check if the referenced assets actually exist"""
    project_dir = os.path.dirname(__file__)
    
    results = {
        'images': {'found': [], 'missing': []},
        'sounds': {'found': [], 'missing': []},
        'music': {'found': [], 'missing': []},
        'other': {'found': [], 'missing': []}
    }
    
    # Common base directories to check
    base_dirs = [
        '',  # Current directory
        'assets/',
        'Assets/',
        'sprites/',
        'Sprites/'
    ]
    
    # Check each asset type
    for asset_type, assets in found_assets.items():
        for asset in assets:
            found = False
            
            # Try different base directories
            for base_dir in base_dirs:
                path = os.path.join(project_dir, base_dir, asset)
                if os.path.exists(path):
                    results[asset_type]['found'].append(asset)
                    found = True
                    break
            
            if not found:
                results[asset_type]['missing'].append(asset)
    
    return results

def generate_missing_assets(missing_assets):
    """Generate placeholder files for missing assets"""
    project_dir = os.path.dirname(__file__)
    
    # Create needed directories
    os.makedirs(os.path.join(project_dir, 'assets', 'sounds'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'assets', 'music'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'assets', 'images'), exist_ok=True)
    
    # Generate placeholder images
    pygame.init()
    for image in missing_assets['images']:
        # Try to extract the directory part
        directory = os.path.dirname(image)
        if directory:
            os.makedirs(os.path.join(project_dir, directory), exist_ok=True)
        
        # Create a placeholder image
        img = pygame.Surface((32, 32))
        img.fill((255, 0, 255))  # Magenta
        
        # Draw a pattern to indicate it's a placeholder
        pygame.draw.line(img, (0, 0, 0), (0, 0), (31, 31), 2)
        pygame.draw.line(img, (0, 0, 0), (0, 31), (31, 0), 2)
        
        # Save the image
        try:
            path = os.path.join(project_dir, image)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pygame.image.save(img, path)
            print(f"Created placeholder image: {path}")
        except Exception as e:
            print(f"Failed to create image {path}: {e}")
    
    # Generate placeholder sound files
    import wave
    import struct
    
    def create_empty_wav(filepath, duration=0.5):
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        channels = 1
        sample_width = 2
        framerate = 44100
        frames = int(framerate * duration)
        
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(framerate)
            
            for _ in range(frames):
                wav_file.writeframes(struct.pack('h', 0))
    
    for sound in missing_assets['sounds']:
        path = os.path.join(project_dir, sound)
        try:
            create_empty_wav(path)
            print(f"Created placeholder sound: {path}")
        except Exception as e:
            print(f"Failed to create sound {path}: {e}")
    
    # Create placeholder music files (empty WAV)
    for music in missing_assets['music']:
        # Just create as WAV for simplicity
        if not music.lower().endswith('.wav'):
            base = os.path.splitext(music)[0]
            music = base + '.wav'
            
        path = os.path.join(project_dir, music)
        try:
            create_empty_wav(path, duration=1.0)
            print(f"Created placeholder music: {path}")
        except Exception as e:
            print(f"Failed to create music {path}: {e}")
    
    return True

def main():
    print("=== Asset Validation Tool ===\n")
    
    # Scan for assets referenced in code
    found_assets = scan_for_assets()
    
    # Print summary of found asset references
    print("\nFound asset references:")
    print(f"Images: {len(found_assets['images'])}")
    print(f"Sounds: {len(found_assets['sounds'])}")
    print(f"Music: {len(found_assets['music'])}")
    print(f"Other: {len(found_assets['other'])}")
    
    # Verify which assets exist
    results = verify_assets_exist(found_assets)
    
    # Print summary of verification
    print("\nAsset verification results:")
    print(f"Images: {len(results['images']['found'])} found, {len(results['images']['missing'])} missing")
    print(f"Sounds: {len(results['sounds']['found'])} found, {len(results['sounds']['missing'])} missing")
    print(f"Music: {len(results['music']['found'])} found, {len(results['music']['missing'])} missing")
    
    # Report missing assets
    if results['images']['missing'] or results['sounds']['missing'] or results['music']['missing']:
        print("\nMissing assets:")
        if results['images']['missing']:
            print("\nMissing images:")
            for img in results['images']['missing']:
                print(f"  - {img}")
                
        if results['sounds']['missing']:
            print("\nMissing sounds:")
            for sound in results['sounds']['missing']:
                print(f"  - {sound}")
                
        if results['music']['missing']:
            print("\nMissing music:")
            for music in results['music']['missing']:
                print(f"  - {music}")
        
        # Generate placeholders for missing assets
        print("\nDo you want to generate placeholder files for missing assets? (y/n)")
        choice = input().lower()
        
        if choice == 'y':
            generate_missing_assets(results)
            print("\nPlaceholder assets have been generated.")
        else:
            print("No placeholder assets were generated.")
    else:
        print("\nAll referenced assets were found!")
    
    print("\nAsset validation complete!")

if __name__ == "__main__":
    main()
