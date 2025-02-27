import sys
import subprocess
import os

def check_and_install_package(package_name):
    """Check if a package is installed, and install it if it's not"""
    print(f"Checking for {package_name}...")
    
    try:
        __import__(package_name)
        print(f"✓ {package_name} is already installed.")
        return True
    except ImportError:
        print(f"✗ {package_name} is not installed.")
        
        # Ask if user wants to install
        response = input(f"Would you like to install {package_name}? (y/n): ").strip().lower()
        if response != 'y':
            return False
            
        print(f"Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✓ Successfully installed {package_name}")
            return True
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package_name}. Please install it manually.")
            return False

def main():
    """Check and install all required packages"""
    required_packages = [
        'pygame'
    ]
    
    print("====================================")
    print("Game Dependencies Installation")
    print("====================================")
    
    # Check Python version
    py_version = sys.version_info
    print(f"Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 7):
        print("Warning: This game requires Python 3.7 or higher.")
    
    # Check and install packages
    all_installed = True
    for package in required_packages:
        if not check_and_install_package(package):
            all_installed = False
    
    if all_installed:
        print("\nAll dependencies are installed! You can now run the game.")
        print("To start the game, run: python main.py")
    else:
        print("\nSome dependencies could not be installed. The game may not run correctly.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
