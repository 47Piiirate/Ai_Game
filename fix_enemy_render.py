"""
Script to fix the Enemy.render() method to accept a camera_offset parameter
"""
import os
import importlib

def fix_enemy_render():
    """
    Updates the Enemy.render() method to accept a camera_offset parameter
    """
    # Find the correct enemy.py file location
    possible_locations = [
        "entities/enemy.py",
        "enemy.py"
    ]
    
    enemy_file_path = None
    for loc in possible_locations:
        if os.path.exists(loc):
            enemy_file_path = loc
            break
    
    if not enemy_file_path:
        print("Error: Could not find enemy.py file.")
        return False
    
    print(f"Found enemy file at: {enemy_file_path}")
    
    # Read the current file content
    with open(enemy_file_path, 'r') as file:
        content = file.read()
    
    # Check if the render method already has the camera_offset parameter
    if "def render(self, screen, camera_offset=(0, 0)):" in content:
        print("Enemy.render() already has camera_offset parameter.")
        return True
    
    # Replace the render method
    old_method = "def render(self, screen):"
    new_method = "def render(self, screen, camera_offset=(0, 0)):"
    
    if old_method in content:
        updated_content = content.replace(old_method, new_method)
        
        # Also make sure the implementation uses the camera_offset
        if "screen.blit(image, self.rect)" in updated_content:
            updated_content = updated_content.replace(
                "screen.blit(image, self.rect)", 
                "screen.blit(image, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))"
            )
        elif "screen.blit(image, (self.rect.x, self.rect.y))" in updated_content:
            updated_content = updated_content.replace(
                "screen.blit(image, (self.rect.x, self.rect.y))", 
                "screen.blit(image, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))"
            )
        
        # Write the updated content back to the file
        with open(enemy_file_path, 'w') as file:
            file.write(updated_content)
        
        print(f"Updated Enemy.render() method in {enemy_file_path}")
        return True
    
    print(f"Could not find Enemy.render() method in {enemy_file_path}")
    
    # If we can't find the method to replace, let's check if we can add a complete replacement
    # by looking for class Enemy definition
    class_def = "class Enemy(AnimatedSprite):"
    
    if class_def in content:
        # Find class Enemy definition
        class_index = content.find(class_def)
        if class_index != -1:
            # Complete replacement render method to add
            render_method = """
    def render(self, screen, camera_offset=(0, 0)):
        \"\"\"Render the enemy with camera offset\"\"\"
        image = self.get_current_frame()
        if image:
            # Apply camera offset
            render_x = self.rect.x - camera_offset[0]
            render_y = self.rect.y - camera_offset[1]
            screen.blit(image, (render_x, render_y))
"""
            
            # Find a good place to insert the method (after __init__ or another method)
            lines = content.split('\n')
            new_lines = []
            found_class = False
            block_level = 0
            added_method = False
            
            for line in lines:
                new_lines.append(line)
                
                # Track if we're inside the Enemy class
                if class_def in line:
                    found_class = True
                    block_level = line.find(class_def)
                    continue
                
                if found_class and not added_method:
                    # Look for the end of a method definition
                    if line.strip() == "" and block_level > 0:
                        # Add our method after a blank line
                        indented_method = render_method.replace('\n    ', f'\n{" " * (block_level + 4)}')
                        new_lines.append(indented_method)
                        added_method = True
            
            if added_method:
                # Write the updated content back
                with open(enemy_file_path, 'w') as file:
                    file.write('\n'.join(new_lines))
                
                print(f"Added render method to Enemy class in {enemy_file_path}")
                return True
    
    # If we got here, we couldn't fix it automatically
    print("Could not automatically fix Enemy.render() method.")
    print("Please add the following method to your Enemy class:")
    print("""
    def render(self, screen, camera_offset=(0, 0)):
        \"\"\"Render the enemy with camera offset\"\"\"
        image = self.get_current_frame()
        if image:
            # Apply camera offset
            render_x = self.rect.x - camera_offset[0]
            render_y = self.rect.y - camera_offset[1]
            screen.blit(image, (render_x, render_y))
    """)
    
    return False

def reload_enemy_module():
    """Try to reload the enemy module if it's already been imported"""
    try:
        # Try to find and reload any imported enemy module
        for module_name in list(sys.modules.keys()):
            if module_name.endswith('enemy') or module_name.endswith('entities.enemy'):
                module = sys.modules[module_name]
                importlib.reload(module)
                print(f"Reloaded module: {module_name}")
    except Exception as e:
        print(f"Error reloading modules: {e}")

if __name__ == "__main__":
    import sys
    
    print("Fixing Enemy.render() method to accept camera_offset parameter...")
    if fix_enemy_render():
        print("Fix applied successfully.")
        reload_enemy_module()
        print("Try running your game now with 'python main.py'")
    else:
        print("Fix could not be applied automatically.")
