import os

def create_directories():
    # Define the sound directory structure - updated to match the paths in the warnings
    sound_dirs = [
        "assets",
        "assets/sounds",
        "assets/music",
        "assets/images"
    ]
    
    # Create the directories if they don't exist
    for directory in sound_dirs:
        dir_path = os.path.join(os.path.dirname(__file__), directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")
        else:
            print(f"Directory already exists: {dir_path}")

if __name__ == "__main__":
    create_directories()
    print("Sound directory structure created successfully!")
