import os
import sys
import shutil
import re

def patch_asset_manager():
    """
    Create a patched version of the asset_manager.py file that adds better error
    handling to prevent NoneType errors when loading images
    """
    # Path to the original file
    original_file = os.path.join(os.path.dirname(__file__), "asset_manager.py")
    
    # Path to the backup file
    backup_file = os.path.join(os.path.dirname(__file__), "asset_manager.py.bak")
    
    # Check if the original file exists
    if not os.path.exists(original_file):
        print(f"Error: Could not find {original_file}")
        return False
    
    # Create a backup of the original file if it doesn't already exist
    if not os.path.exists(backup_file):
        try:
            shutil.copy2(original_file, backup_file)
            print(f"Created backup: {backup_file}")
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    else:
        print(f"Backup already exists: {backup_file}")
    
    try:
        # Read the original file
        with open(original_file, 'r') as f:
            content = f.read()
        
        # Look for the AssetManager class definition
        if 'class AssetManager' not in content:
            print("Could not find AssetManager class in asset_manager.py")
            return False
            
        # First, check if our patch is already applied
        if 'fallback = pygame.Surface((32, 32))' in content:
            print("The asset manager appears to already be patched.")
            return True
        
        # Find the load_image method and replace it with our patched version
        # Different approach that doesn't rely on specific formatting
        patched_code = """
    def load_image(self, path):
        \"\"\"Load an image and return a pygame surface or a fallback if it fails.\"\"\"
        try:
            full_path = os.path.join(os.path.dirname(__file__), path)
            
            # Check if file exists
            if not os.path.exists(full_path):
                print(f"Warning: Image file does not exist: {full_path}")
                # Return a fallback image (small colored square)
                fallback = pygame.Surface((32, 32))
                fallback.fill((255, 0, 255))  # Magenta for visibility
                return fallback
            
            # Try to load the image
            image = pygame.image.load(full_path)
            
            # Check if image is None
            if image is None:
                print(f"Warning: Failed to load image, returned None: {path}")
                fallback = pygame.Surface((32, 32))
                fallback.fill((255, 0, 255))  # Magenta for visibility
                return fallback
                
            # Test getting the rect
            try:
                image.get_rect()
            except Exception as e:
                print(f"Warning: Invalid image (get_rect failed): {path}, Error: {e}")
                fallback = pygame.Surface((32, 32))
                fallback.fill((255, 0, 255))  # Magenta for visibility
                return fallback
                
            print(f"Loaded image: {path}")
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Return a fallback image (small colored square)
            fallback = pygame.Surface((32, 32))
            fallback.fill((255, 0, 255))  # Magenta for visibility
            return fallback
"""
        
        # Use a more flexible approach to find and replace the load_image method
        image_method_pattern = r'([ \t]*)def load_image\([^)]*\):.*?(?=\n\1def|\n\s*class|\Z)'
        
        match = re.search(image_method_pattern, content, re.DOTALL)
        if match:
            indent = match.group(1)  # Capture the indentation
            # Adjust patched_code indentation to match
            adjusted_patched_code = patched_code.replace('\n    ', f'\n{indent}')
            
            # Replace the method
            patched_content = content[:match.start()] + adjusted_patched_code + content[match.end():]
            
            # Write the patched content back
            with open(original_file, 'w') as f:
                f.write(patched_content)
                
            print(f"Successfully patched {original_file} with improved error handling")
            return True
        else:
            # Create a new load_image method if one doesn't exist
            class_pattern = r'(class AssetManager.*?:.*?\n)(.*?)(?=\n\s*class|\Z)'
            match = re.search(class_pattern, content, re.DOTALL)
            
            if match:
                class_def = match.group(1)
                class_body = match.group(2)
                
                # Find the indentation level of the class body
                lines = class_body.split('\n')
                indent = '    '  # Default indentation
                for line in lines:
                    if line.strip() and not line.startswith('\n'):
                        indent_match = re.match(r'^(\s+)', line)
                        if indent_match:
                            indent = indent_match.group(1)
                            break
                
                # Adjust patched_code indentation to match
                adjusted_patched_code = patched_code.replace('\n    ', f'\n{indent}')
                
                # Add the method to the class
                new_content = content[:match.end()] + adjusted_patched_code + content[match.end():]
                
                # Write the updated content
                with open(original_file, 'w') as f:
                    f.write(new_content)
                    
                print(f"Added load_image method to {original_file} with improved error handling")
                return True
            else:
                print("Could not find the AssetManager class structure")
                return False
            
    except Exception as e:
        print(f"Error patching asset_manager.py: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if patch_asset_manager():
        print("Asset manager patched successfully. This should prevent 'NoneType' errors when loading images.")
    else:
        print("Failed to patch asset manager. Please check the error messages above.")
