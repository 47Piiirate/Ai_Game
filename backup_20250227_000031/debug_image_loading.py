import os
import pygame
import sys
from pprint import pprint

def debug_image_loading():
    """Debug function to check all images in the Sprites directory."""
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    # Dictionary to store results
    results = {
        "successful": [],
        "failed": []
    }
    
    # Walk through all files in the Sprites directory
    sprites_dir = os.path.join(os.path.dirname(__file__), "Sprites")
    for root, _, files in os.walk(sprites_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, os.path.dirname(__file__))
                
                try:
                    img = pygame.image.load(full_path)
                    if img is None:
                        results["failed"].append({
                            "path": relative_path,
                            "error": "Image loaded as None"
                        })
                    else:
                        try:
                            rect = img.get_rect()
                            results["successful"].append({
                                "path": relative_path,
                                "size": rect.size
                            })
                        except Exception as e:
                            results["failed"].append({
                                "path": relative_path,
                                "error": f"get_rect() failed: {str(e)}"
                            })
                except Exception as e:
                    results["failed"].append({
                        "path": relative_path,
                        "error": str(e)
                    })
    
    return results

if __name__ == "__main__":
    results = debug_image_loading()
    
    print("\n=== DEBUG IMAGE LOADING RESULTS ===\n")
    
    print(f"Total images checked: {len(results['successful']) + len(results['failed'])}")
    print(f"Successful: {len(results['successful'])}")
    print(f"Failed: {len(results['failed'])}")
    
    if results['failed']:
        print("\n=== FAILED IMAGES ===")
        pprint(results['failed'])
    
    pygame.quit()
