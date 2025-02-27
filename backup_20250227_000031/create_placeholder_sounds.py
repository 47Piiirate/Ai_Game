import os
import wave
import struct

def create_empty_wav(filename, duration=0.5):
    """Create an empty WAV file with the given filename and duration."""
    # Parameters
    channels = 1
    sample_width = 2  # 2 bytes = 16 bits
    framerate = 44100  # CD quality
    frames = int(framerate * duration)
    
    filepath = os.path.join(os.path.dirname(__file__), filename)
    directory = os.path.dirname(filepath)
    
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Create WAV file
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(framerate)
        
        # Generate silent audio data
        for _ in range(frames):
            wav_file.writeframes(struct.pack('h', 0))
            
    print(f"Created placeholder sound: {filepath}")

def main():
    # List of missing sound files from the error messages - updated based on asset paths in main.py
    sound_files = [
        "assets/sounds/jump.wav",
        "assets/sounds/dash.wav",
        "assets/sounds/attack.wav",
        "assets/sounds/hit.wav",
        "assets/sounds/parry.wav",
        "assets/sounds/collect.wav",
        "assets/sounds/death.wav",
        "assets/sounds/menu_select.wav",
        "assets/sounds/boss_hit.wav",
        "assets/sounds/ability_unlock.wav"
    ]
    
    for sound_file in sound_files:
        create_empty_wav(sound_file)

if __name__ == "__main__":
    main()
    print("All placeholder sound files created successfully!")
