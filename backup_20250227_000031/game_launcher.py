"""
Game launcher that ensures the environment is set up correctly before running the game
"""

import os
import sys
import subprocess
import importlib.util
import pygame

# Function to check if a module is available
def module_available(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None

# Initialize pygame so we can use it for version checking
pygame.init()
print(f"pygame {pygame.version.ver} (SDL {pygame.version.SDL})")
print(f"Hello from the pygame community. https://www.pygame.org/contribute.html")

# Check for required modules
required_modules = ["pygame", "json", "time", "os", "sys", "re", "shutil"]
missing_modules = []

for module in required_modules:
    if not module_available(module):
        missing_modules.append(module)

if missing_modules:
    print("Error: Missing required Python modules:")
    for module in missing_modules:
        print(f"  - {module}")
    print("\nPlease install missing modules using pip:")
    print(f"pip install {' '.join(missing_modules)}")
    sys.exit(1)

# Check and set up the asset structure
try:
    from asset_structure import check_asset_structure, create_default_readme_files
    check_asset_structure()
    create_default_readme_files()
except ImportError:
    print("Warning: Could not import asset_structure module. Skipping asset structure check.")
except Exception as e:
    print(f"Warning: Error during asset structure setup: {e}")

# Check and patch asset_manager.py if needed
try:
    from asset_manager_patch import patch_asset_manager
    patch_asset_manager()
except ImportError:
    print("Warning: Could not import asset_manager_patch module. Skipping asset manager patch.")
except Exception as e:
    print(f"Warning: Error during asset manager patching: {e}")

print("Starting game...")

# Run the main game script
try:
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("Error: main.py file not found. Cannot start the game.")
        sys.exit(1)
        
    # Import and run the main game module
    import main
except Exception as e:
    print(f"Error starting game: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
