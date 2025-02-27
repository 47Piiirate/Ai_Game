import sys
import os
import subprocess

print("=== Python Environment Check ===")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

# Check for pygame in this Python environment
try:
    import pygame
    print(f"Pygame is installed: {pygame.__version__}")
except ImportError:
    print("Pygame is NOT installed in this Python environment")

# List all Python installations
print("\nLooking for Python installations:")
python_commands = ["python", "python3", "py", "py -3"]
for cmd in python_commands:
    try:
        if " " in cmd:
            cmd_parts = cmd.split()
            result = subprocess.run(cmd_parts + ["--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  check=False)
        else:
            result = subprocess.run([cmd, "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  check=False)
            
        if result.returncode == 0:
            print(f"{cmd}: {result.stdout.strip()}")
            
            # Check if pygame is installed in this Python
            pygame_check_cmd = "import pygame; print(f'Pygame {pygame.__version__}')"
            if " " in cmd:
                cmd_parts = cmd.split()
                result = subprocess.run(cmd_parts + ["-c", pygame_check_cmd], 
                                      capture_output=True, 
                                      text=True, 
                                      check=False)
            else:
                result = subprocess.run([cmd, "-c", pygame_check_cmd], 
                                      capture_output=True, 
                                      text=True, 
                                      check=False)
                
            if result.returncode == 0:
                print(f"  - Has pygame: {result.stdout.strip()}")
            else:
                print(f"  - No pygame installed")
    except Exception as e:
        print(f"{cmd}: Not found or error ({e})")

print("\n=== Suggested Fix ===")
print("Install pygame for the current Python:")
print(f"{sys.executable} -m pip install pygame")
