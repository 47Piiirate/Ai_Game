"""
Pure Python implementation of the physics engine.
The C extension has been removed for simplicity.
"""
import pygame

# Simply set the flag to False since we're not using the C extension
using_c_extension = False
print("Using Python implementation for physics")

def sweep_test(player_x, player_y, player_width, player_height, velocity_x, velocity_y, obstacles):
    """
    Perform a sweep test for collision detection.
    
    Args:
        player_x, player_y: Player position
        player_width, player_height: Player dimensions
        velocity_x, velocity_y: Player velocity
        obstacles: List of obstacle rects as (x, y, width, height) tuples
    
    Returns:
        Tuple of (new_x, new_y, collided_x, collided_y)
    """
    # Python implementation (simplified)
    final_x = player_x + velocity_x
    final_y = player_y + velocity_y
    collided_x = False
    collided_y = False
    
    # If there are no obstacles, just return the final position with no collisions
    if not obstacles:
        return final_x, final_y, collided_x, collided_y
    
    # Create player rect at new position
    new_player_rect_x = pygame.Rect(final_x, player_y, player_width, player_height)
    new_player_rect_y = pygame.Rect(player_x, final_y, player_width, player_height)
    
    # Check for collisions in X direction
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(*obstacle)
        if new_player_rect_x.colliderect(obstacle_rect):
            collided_x = True
            if velocity_x > 0:
                final_x = obstacle_rect.left - player_width
            elif velocity_x < 0:
                final_x = obstacle_rect.right
    
    # Check for collisions in Y direction
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(*obstacle)
        if new_player_rect_y.colliderect(obstacle_rect):
            collided_y = True
            if velocity_y > 0:
                final_y = obstacle_rect.top - player_height
            elif velocity_y < 0:
                final_y = obstacle_rect.bottom
    
    return final_x, final_y, collided_x, collided_y

def check_on_ground(player_x, player_y, player_width, player_height, obstacles, check_distance=1.0):
    """
    Check if the player is on the ground.
    
    Args:
        player_x, player_y: Player position
        player_width, player_height: Player dimensions
        obstacles: List of obstacle rects as (x, y, width, height) tuples
        check_distance: Distance to check below player
    
    Returns:
        Boolean indicating if player is on the ground
    """
    # If there are no obstacles, player can't be on ground
    if not obstacles:
        return False
        
    ground_check_rect = pygame.Rect(
        player_x, player_y + player_height,
        player_width, check_distance
    )
    
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(*obstacle)
        if ground_check_rect.colliderect(obstacle_rect):
            return True
    
    return False
