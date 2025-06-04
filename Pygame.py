import pygame
import math
import sys

# Gameboard
WIDTH, HEIGHT = 800, 600
# Colors
WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)

# Initialize Pygame
pygame.init()
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Robot Navigation Game")
except pygame.error as e:
    print(f"Failed to initialize Pygame: {e}")
    sys.exit(1)

clock = pygame.time.Clock()

# Robot properties
robot_x, robot_y = 100, 100
robot_angle = 0
robot_speed = 5 

# Target properties
target_x, target_y = 200, 500

# Obstacle properties
obstacle_x, obstacle_y = WIDTH/2, HEIGHT/2
obstacle_radius = 50

# Angle from robot to target
def calculate_angle(target_x, target_y):
    var = robot_x, robot_y, robot_angle
    angle_to_target = math.degrees(math.atan2(target_y - robot_y, target_x - robot_x))
    angle_difference = (angle_to_target - robot_angle + 360) % 360
    return angle_difference if angle_difference <= 180 else angle_difference - 360

# Check for whether the path is blocked
def is_path_blocked(target_x, target_y, threshold=60):
    distance_to_line = abs((target_y - robot_y) * obstacle_x - (target_x - robot_x) * obstacle_y + target_x * robot_y - target_y * robot_x) / math.hypot(target_x - robot_x, target_y - robot_y)
    return distance_to_line < threshold and min(robot_x, target_x) < obstacle_x < max(robot_x, target_x)

# Calculate simple detour point
def find_detour(target_x, target_y, detour_distance=100):
    obstacle_angle = math.atan2(obstacle_y - robot_y, obstacle_x - robot_x)
    detour_angle = obstacle_angle + math.radians(90)
    detour_x = obstacle_x + detour_distance * math.cos(detour_angle)
    detour_y = obstacle_y + detour_distance * math.sin(detour_angle)
    return detour_x, detour_y

points = 0

# Main Loop
running = True
waypoint = None
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill(WHITE)
    
    # Draw target, obstacle, and robot
    pygame.draw.circle(screen, RED, (target_x, target_y), 10)  # Target
    pygame.draw.circle(screen, BLACK, (obstacle_x, obstacle_y), obstacle_radius)  # Obstacle
    pygame.draw.circle(screen, BLUE, (int(robot_x), int(robot_y)), 10)  # Robot
    
    # Draw angle direction line
    direction_x = robot_x + 20 * math.cos(math.radians(robot_angle))
    direction_y = robot_y + 20 * math.sin(math.radians(robot_angle))
    pygame.draw.line(screen, BLUE, (robot_x, robot_y), (direction_x, direction_y), 2)
    
    # Check if obstacle is blocking path
    if waypoint is None and is_path_blocked(target_x, target_y):
        print("Obstacle detected! Finding detour...")
        waypoint = find_detour(target_x, target_y)
    
    # Choose current destination (waypoint or final target)
    if waypoint:
        current_target_x, current_target_y = waypoint
        if math.hypot(robot_x - waypoint[0], robot_y - waypoint[1]) < 10:  # Reached waypoint
            print("Waypoint reached, resuming to target!")
            waypoint = None
    else:
        current_target_x, current_target_y = target_x, target_y
    
    # Calculate angle difference and move
    angle_to_turn = calculate_angle(current_target_x, current_target_y)
    
    if abs(angle_to_turn) > 2:  # Rotate first
        robot_angle += 2 * (1 if angle_to_turn > 0 else -1)
    else:  # Move forward
        robot_x += robot_speed * math.cos(math.radians(robot_angle))
        robot_y += robot_speed * math.sin(math.radians(robot_angle))
    
    # Stop when reaching the target
    if math.hypot(robot_x - target_x, robot_y - target_y) < 10:
        print("Target reached!")
        points += 1

        if points == 10:
            break

        if target_x == 100:
            target_x = 500
            target_y = 200
        else:
            target_x = 100
            target_y = 100
        
        # running = False

    
    pygame.display.flip()
    clock.tick(30)  # 30 FPS

# Clean up
pygame.quit()
sys.exit()