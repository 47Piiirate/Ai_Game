"""
Script to fix import errors after reorganizing the codebase
"""
import os
import re

# Dictionary mapping files to their new module paths
file_to_module = {
    'app.py': 'core.app',
    'game.py': 'core.game',
    'game_state.py': 'core.game_state',
    'config.py': 'core.config',
    'player.py': 'entities.player',
    'enemy.py': 'entities.enemy',
    'npc.py': 'entities.npc',
    'collectible.py': 'entities.collectible',
    'animation.py': 'systems.animation',
    'physics.py': 'systems.physics',
    'camera.py': 'systems.camera',
    'achievements.py': 'systems.achievements',
    'inventory.py': 'systems.inventory',
    'combat_manager.py': 'systems.combat_manager',
    'quest_system.py': 'systems.quest_system',
    'save_manager.py': 'systems.save_manager',
    'tilemap.py': 'graphics.tilemap',
    'particles.py': 'graphics.particles',
    'ui.py': 'graphics.ui',
    'minimap.py': 'graphics.minimap',
    'asset_manager.py': 'utils.asset_manager',
    'asset_loader.py': 'utils.asset_loader',
    'logger.py': 'utils.logger'
}

# Directory structure to scan
directories = ['core', 'entities', 'systems', 'graphics', 'utils']

def update_imports(file_path):
    """Update import statements in a file to use the new module structure"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Track if file was modified
    modified = False
    new_content = content

    # Check for each potential import
    for filename, module_path in file_to_module.items():
        module_name = os.path.splitext(filename)[0]
        
        # Update "from X import Y" statements
        old_import = f"from {module_name} import"
        new_import = f"from {module_path} import"
        if old_import in new_content:
            new_content = new_content.replace(old_import, new_import)
            modified = True
            
        # Update "import X" statements
        old_import = f"import {module_name}"
        new_import = f"import {module_path}"
        
        # Only replace if it's a complete import statement (not part of another import)
        # This uses regex to match the import at word boundaries
        pattern = r'\b' + re.escape(old_import) + r'\b'
        if re.search(pattern, new_content):
            new_content = re.sub(pattern, new_import, new_content)
            modified = True
    
    # Save changes if modified
    if modified:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    
    return False

def fix_game_py():
    """Fix the specific import error in game.py"""
    game_path = os.path.join('core', 'game.py')
    if os.path.exists(game_path):
        with open(game_path, 'r') as f:
            content = f.read()
        
        # Replace the problematic import line
        if 'from entities.enemy import Enemy, Boss' in content:
            content = content.replace(
                'from entities.enemy import Enemy, Boss',
                'from entities.enemy import Enemy'
            )
            
            with open(game_path, 'w') as f:
                f.write(content)
            print(f"Fixed Boss import error in {game_path}")

def scan_directory():
    """Scan directories and fix import statements"""
    fixed_files = []
    
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    if update_imports(file_path):
                        fixed_files.append(file_path)
    
    # Fix main.py too
    if os.path.exists('main.py'):
        if update_imports('main.py'):
            fixed_files.append('main.py')
    
    # Fix the specific error in game.py
    fix_game_py()
    
    return fixed_files

if __name__ == '__main__':
    print("Fixing import statements after reorganization...")
    fixed = scan_directory()
    
    if fixed:
        print(f"Fixed imports in {len(fixed)} files:")
        for file in fixed:
            print(f"  - {file}")
    else:
        print("No import issues were found.")
        
    print("\nScript complete. Try running the game with: python main.py")
