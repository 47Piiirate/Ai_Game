import sys
import subprocess
import os

def find_python_with_pygame():
    """Find a Python interpreter with pygame installed"""
    python_commands = ["python", "python3", "py", "py -3"]
    
    for cmd in python_commands:
        try:
            cmd_parts = cmd.split() if " " in cmd else [cmd]
            result = subprocess.run(cmd_parts + ["-c", "import pygame"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            if result.returncode == 0:
                print(f"Found pygame in {cmd}")
                return cmd
        except Exception:
            pass
    
    return None

def main():
    print("=== Metroidvania Game Launcher ===")
    
    # Try to find Python with pygame
    python_cmd = find_python_with_pygame()
    
    if python_cmd:
        print(f"Running game with {python_cmd}...")
        
        # Build command
        cmd_parts = python_cmd.split() if " " in python_cmd else [python_cmd]
        cmd_parts.append("main.py")
        
        # Execute the game
        try:
            subprocess.run(cmd_parts)
        except Exception as e:
            print(f"Error launching game: {e}")
    else:
        print("Could not find Python with pygame installed.")
        
        # Offer to install pygame
        response = input("Would you like to install pygame now? (y/n): ")
        if response.lower() == 'y':
            print("Installing pygame...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "pygame"])
                print("\nRunning the game...")
                subprocess.run([sys.executable, "main.py"])
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("\nPlease install pygame manually with:")
            print("pip install pygame")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
