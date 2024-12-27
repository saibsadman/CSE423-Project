from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_COLS = WINDOW_WIDTH // GRID_SIZE
GRID_ROWS = WINDOW_HEIGHT // GRID_SIZE

# Game variables
snake = [{'x': GRID_COLS // 2, 'y': GRID_ROWS // 2}]
food = {'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)}
poisonous_food = None
shell = None
shell_active = False
shell_timer = None
direction = 'RIGHT'
game_over = False
score = 0
food_count = 0
poisonous_food_eaten = False
paused = False
startup_phase = True  # Flag to track if the startup phase is active
countdown = 3  # Countdown for starting the game
start_time = time.time()  # Initialize the start time to track when the startup phase begins
speed = 200  # Initial snake speed in milliseconds
OBSTACLE_COUNT = 3
obstacles = []
# Teleportation portal variables
first_portal = None
second_portal = None
portal_running = False
timer_for_portal = None


# Colors
SNAKE_COLOR = (0.0, 0.8, 0.0)  # Dark Green
FOOD_COLOR = (1.0, 0.0, 0.0)   # Red
POISONOUS_FOOD_COLOR = (0.0, 0.0, 1.0)  # Blue
SHELL_COLOR = (1.0, 1.0, 0.0)  # Yellow
SCORE_COLOR = (1.0, 1.0, 1.0)  # White

# Draw a rounded snake segment using points
def draw_segment(x, y, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    center_x = x * GRID_SIZE + GRID_SIZE / 2
    center_y = y * GRID_SIZE + GRID_SIZE / 2
    radius = GRID_SIZE / 2
    for i in range(-int(radius), int(radius) + 1):
        for j in range(-int(radius), int(radius) + 1):
            if i**2 + j**2 <= radius**2:  # Check if within circle
                glVertex2f(center_x + i, center_y + j)
    glEnd()

# Draw a square for the food using points
def draw_food(x, y, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    start_x = x * GRID_SIZE
    start_y = y * GRID_SIZE
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            glVertex2f(start_x + i, start_y + j)
    glEnd()


def draw_line(x0, y0, x1, y1, color=(1.0, 0.0, 0.0)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    
    # Identify the line's zone
    dx = x1 - x0
    dy = y1 - y0
    
    # Determine zone
    zone = 0
    if abs(dx) >= abs(dy):  # |slope| <= 1
        if dx >= 0 and dy >= 0:  # Zone 0
            zone = 0
        elif dx <= 0 and dy >= 0:  # Zone 3
            zone = 3
        elif dx >= 0 and dy <= 0:  # Zone 7
            zone = 7
        else:  # Zone 4
            zone = 4
    else:  # |slope| > 1
        if dx >= 0 and dy >= 0:  # Zone 1
            zone = 1
        elif dx <= 0 and dy >= 0:  # Zone 2
            zone = 2
        elif dx >= 0 and dy <= 0:  # Zone 6
            zone = 6
        else:  # Zone 5
            zone = 5

    # Convert to Zone 0
    def to_zone0(x, y, zone):
        if zone == 0:
            return x, y
        elif zone == 1:
            return y, x
        elif zone == 2:
            return y, -x
        elif zone == 3:
            return -x, y
        elif zone == 4:
            return -x, -y
        elif zone == 5:
            return -y, -x
        elif zone == 6:
            return -y, x
        elif zone == 7:
            return x, -y

    # Convert from Zone 0 to original zone
    def from_zone0(x, y, zone):
        if zone == 0:
            return x, y
        elif zone == 1:
            return y, x
        elif zone == 2:
            return -y, x
        elif zone == 3:
            return -x, y
        elif zone == 4:
            return -x, -y
        elif zone == 5:
            return -y, -x
        elif zone == 6:
            return y, -x
        elif zone == 7:
            return x, -y

    # Convert endpoints to Zone 0
    x0_zone, y0_zone = to_zone0(x0, y0, zone)
    x1_zone, y1_zone = to_zone0(x1, y1, zone)

    # Apply midpoint algorithm in Zone 0
    dx = x1_zone - x0_zone
    dy = y1_zone - y0_zone
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)

    x, y = x0_zone, y0_zone
    while x <= x1_zone:
        # Convert point back to original zone and draw
        orig_x, orig_y = from_zone0(x, y, zone)
        glVertex2f(orig_x, orig_y)
        if d <= 0:
            d += incrE
        else:
            d += incrNE
            y += 1
        x += 1

    glEnd()


# Draw a triangular obstacle using three lines
# Draw a triangular obstacle using three lines
def draw_obstacle(x, y, size, color=(1.0, 0.0, 0.0)):  # Bright red color
    half_size = size // 2
    draw_line(x - half_size, y - half_size, x + half_size, y - half_size, color)  # Bottom side
    draw_line(x - half_size, y - half_size, x, y + half_size, color)  # Left side
    draw_line(x, y + half_size, x + half_size, y - half_size, color)  # Right side



# Draw a portal (shell) using the midpoint circle algorithm from code 1
def draw_circle(x, y, radius, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    
    # Midpoint Circle Algorithm
    centerX = x
    centerY = y
    d = 1 - radius
    cx = 0
    cy = radius

    while cy > cx:
        glVertex2f(cx + centerX, cy + centerY)
        glVertex2f(cx + centerX, -cy + centerY)
        glVertex2f(-cx + centerX, cy + centerY)
        glVertex2f(-cx + centerX, -cy + centerY)
        glVertex2f(cy + centerX, cx + centerY)
        glVertex2f(cy + centerX, -cx + centerY)
        glVertex2f(-cy + centerX, cx + centerY)
        glVertex2f(-cy + centerX, -cx + centerY)
        if d < 0:
            d += 2 * cx + 3
        else:
            d += 2 * cx - 2 * cy + 5
            cy -= 1
        cx += 1

    glEnd()

#teleportation portals
def draw_teleportation():
    global first_portal, second_portal
    if first_portal and second_portal:
        draw_circle(first_portal['x'] * GRID_SIZE + GRID_SIZE / 2, first_portal['y'] * GRID_SIZE + GRID_SIZE / 2, GRID_SIZE // 2, (0.5, 0.5, 1.0))  # Light blue
        draw_circle(second_portal['x'] * GRID_SIZE + GRID_SIZE / 2, second_portal['y'] * GRID_SIZE + GRID_SIZE / 2, GRID_SIZE // 2, (0.5, 0.5, 1.0))  # Light blue
    
# Render text for the score
def render_text(x, y, text, color):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

startup_messages = [
    ("Game Rules:", (1.0, 1.0, 0.0)),  # Yellow
    ("1. Catch the Red foods", (1.0, 0.0, 0.0)),  
    ("2. Beware of the Blue poisonous food", (0.0, 0.0, 1.0)),  
    ("3. Catch the yellow shell to get back to original shape", (0.0, 1.0, 0.0)),  
    ("4. Speed increases upon scoring 80 points", (0.0, 1.0, 1.0)),
    ("5. Use Teleportation portals to teleport from one location to another", (0.5, 0.8, 0.2)),
    ("6. Avoid the obstacles", (1.0, 0.6, 1.0))

]

# Place random obstacles on the grid
def generate_obstacles():
    global obstacles
    # Update obstacles when food is eaten
    obstacles = [{'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)} for _ in range(3)]

# teleportation portals generation
def portal_generation():
    global first_portal, second_portal, portal_running, timer_for_portal
    first_portal = {'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)}
    second_portal = {'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)}
    portal_running = True
    timer_for_portal = time.time()

# Check if the snake collides with any obstacles
def check_obstacle_collision():
    global game_over, first_portal, second_portal, portal_running
    head = snake[0]
    for obstacle in obstacles:
        if head['x'] == obstacle['x'] and head['y'] == obstacle['y']:
            game_over = True
            # Clear portals when game ends
            first_portal = None
            second_portal = None
            portal_running = False
            print(f"Game Over! Collided with an obstacle. Final Score: {score}")

            
# Display function
def display():
    global game_over, shell, shell_active, startup_phase, countdown, start_time, obstacles

    glClear(GL_COLOR_BUFFER_BIT)

    if startup_phase:
        # Show each startup message
        for i, (message, color) in enumerate(startup_messages):
            render_text(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2 - (i * 30), message, color)
        # Check if we need to start the countdown
        if time.time() - start_time > 5:  # 3 seconds for "Beware" message
            startup_phase = False
            countdown = 3  # Reset countdown
            start_time = time.time()  # Reset the start time for countdown
    elif countdown > 0:
        # Show countdown
        render_text(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2, f"Game will start in {countdown}...", SCORE_COLOR)
        if time.time() - start_time > 1:  # Countdown step every second
            countdown -= 1
            start_time = time.time()  # Reset the start time
    else:
        # Start the game after countdown reaches 0
        # Draw the snake and game objects
        if not game_over:
            # Draw the snake
            for segment in snake:
                draw_segment(segment['x'], segment['y'], SNAKE_COLOR)

            # Draw the food
            draw_food(food['x'], food['y'], FOOD_COLOR)

            # Draw the poisonous food if it exists
            if poisonous_food:
                draw_food(poisonous_food['x'], poisonous_food['y'], POISONOUS_FOOD_COLOR)

            # Draw the shell (portal)
            if shell:
                draw_circle(shell['x'] * GRID_SIZE + GRID_SIZE / 2, shell['y'] * GRID_SIZE + GRID_SIZE / 2, GRID_SIZE, SHELL_COLOR)
            
            for obstacle in obstacles:
                draw_obstacle(obstacle['x'] * GRID_SIZE + GRID_SIZE // 2, obstacle['y'] * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE, (1.0, 0.0, 0.0))  # Bright red
            # Draw teleportation portals only if game is not over
            if portal_running:
                draw_teleportation()


            # Display the score
            render_text(10, WINDOW_HEIGHT - 20, f"Score: {score}", SCORE_COLOR)
            render_text(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 20, "Press P: Pause/Resume", SCORE_COLOR)
        else:
            # Display game over message
            render_text(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2, "Game Over!", SCORE_COLOR)
            render_text(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2 - 40, "Press R to Restart", SCORE_COLOR)
    # Draw teleportation portals
    glutSwapBuffers()

# Move the snake
def move_snake():
    global snake, food, poisonous_food, poisonous_food_timer, shell, shell_active, shell_timer
    global direction, game_over, score, food_count, poisonous_food_eaten, paused, startup_phase, speed
    global first_portal, second_portal, portal_running  # Add these globals

    if game_over or paused or startup_phase:
        return

    # Determine the new head position
    head = snake[0].copy()
    if direction == 'UP':
        head['y'] += 1
    elif direction == 'DOWN':
        head['y'] -= 1
    elif direction == 'LEFT':
        head['x'] -= 1
    elif direction == 'RIGHT':
        head['x'] += 1

    # Check for wall collision
    if head['x'] < 0 or head['x'] >= GRID_COLS or head['y'] < 0 or head['y'] >= GRID_ROWS:
        game_over = True
        # Clear portals when game ends
        first_portal = None
        second_portal = None
        portal_running = False
        print(f"Game Over! Final Score: {score}")
        return

    # Check for self-collision
    if head in snake:
        game_over = True
        # Clear portals when game ends
        first_portal = None
        second_portal = None
        portal_running = False
        print(f"Game Over! Final Score: {score}")
        return
    

    # Move the snake by adding the new head
    snake.insert(0, head)

    # Check if the snake eats the food
    if head['x'] == food['x'] and head['y'] == food['y']:
        # Update food position
        food['x'] = random.randint(0, GRID_COLS - 1)
        food['y'] = random.randint(0, GRID_ROWS - 1)
        score += 10
        food_count += 1
        generate_obstacles()

        # Adjust speed every 200 points
        if score % 80 == 0:
            speed = max(50, speed - 100)  # Reduce speed but not below 50ms


        # Reset poisonous food whenever normal food is eaten
        poisonous_food = None
        poisonous_food_timer = None

        # Generate new poisonous food every 3 regular food items
        if food_count % 3 == 0:
            poisonous_food = {'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)}
            poisonous_food_timer = time.time()

        # Generate shell after every 10 foods
        if food_count % 10 == 0 and not shell_active:
            # Ensure the shell is generated within the grid boundaries
            shell_x = random.randint(0 + (GRID_SIZE // 2), GRID_COLS - 1 - (GRID_SIZE // 2))
            shell_y = random.randint(0 + (GRID_SIZE // 2), GRID_ROWS - 1 - (GRID_SIZE // 2))
            shell = {'x': shell_x, 'y': shell_y}
            shell_active = True
            shell_timer = time.time()  # Start the shell timer

    else:
        # Remove the tail if no food is eaten
        snake.pop()
    check_obstacle_collision()
    # Check if the snake enters the shell
    if shell:
        head_x = head['x'] * GRID_SIZE + GRID_SIZE / 2  # Convert grid coordinates to pixel coordinates
        head_y = head['y'] * GRID_SIZE + GRID_SIZE / 2
        shell_x = shell['x'] * GRID_SIZE + GRID_SIZE / 2
        shell_y = shell['y'] * GRID_SIZE + GRID_SIZE / 2
        distance = ((head_x - shell_x) ** 2 + (head_y - shell_y) ** 2) ** 0.5
        if distance <= GRID_SIZE:  # Check if head is within the shell's radius
            snake = [snake[0]]  # Shrink snake to a single segment
            shell_active = False  # Deactivate shell
            shell = None  # Remove shell from the grid
            food_count = 0  # Reset food count
            score += 5  # Increase score by 5
            shell_timer = None  # Reset the shell timer

    # Check if the shell has expired (10 seconds passed)
    if shell and time.time() - shell_timer > 10:
        shell_active = False  # Deactivate shell
        shell = None  # Remove shell from the grid

    # Check if the snake eats the poisonous food
    if poisonous_food and head['x'] == poisonous_food['x'] and head['y'] == poisonous_food['y']:
        game_over = True
        print(f"Game Over! Final Score: {score}")
        poisonous_food_eaten = True

    # ###snake using the teleportation portal#######
    
    if portal_running:
        if head['x'] == first_portal['x'] and head['y'] == first_portal['y']:
            snake[0] = second_portal  # Teleport snake head to portal B
        elif head['x'] == second_portal['x'] and head['y'] == second_portal['y']:
            snake[0] = first_portal  # Teleport snake head to portal A
    # ##teleportation time expiration
    if portal_running and time.time() - timer_for_portal > 10:
        first_portal = None
        second_portal = None
        portal_running = False

# Keyboard input handler
def keyboard(key, x, y):
    global direction, game_over, paused, portal_running, first_portal, second_portal, timer_for_portal

    if game_over and key == b'r':  # Restart game
        restart_game()
    elif key == b'p':  # Pause/Resume game
        paused = not paused
    elif key == b' ':  # Activate Teleportation Portal
        if not portal_running:  # If portals are not active, activate them
            portal_generation()  # Generate new portals
            timer_for_portal = time.time()  # Start the portal timer
        else:
            first_portal = None  # Deactivate portals
            second_portal = None
            portal_running = False

# Special keyboard input handler for arrow keys
def special_input(key, x, y):
    global direction
    if key == GLUT_KEY_UP and direction != 'DOWN':
        direction = 'UP'
    elif key == GLUT_KEY_DOWN and direction != 'UP':
        direction = 'DOWN'
    elif key == GLUT_KEY_LEFT and direction != 'RIGHT':
        direction = 'LEFT'
    elif key == GLUT_KEY_RIGHT and direction != 'LEFT':
        direction = 'RIGHT'

# Restart the game
def restart_game():
    global snake, food, poisonous_food, shell, shell_active, shell_timer, direction, game_over, score, food_count, poisonous_food_eaten, paused, startup_phase, countdown, start_time, speed
    snake = [{'x': GRID_COLS // 2, 'y': GRID_ROWS // 2}]
    food = {'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)}
    poisonous_food = None
    shell = None
    shell_active = False
    shell_timer = None
    direction = 'RIGHT'
    game_over = False
    score = 0
    food_count = 0
    poisonous_food_eaten = False
    paused = False
    startup_phase = True
    countdown = 3  # Reset countdown
    start_time = time.time()  # Reset start time
    speed = 200  # Reset speed
    

# Timer function for continuous updates
def update(value):
    move_snake()
    glutPostRedisplay()
    glutTimerFunc(speed, update, 0)  # Use dynamic speed

# Initialize OpenGL
def initialize():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)  # Set orthographic view

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow(b"Snake Game with Shell and Poisonous Food")
initialize()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_input)
glutTimerFunc(speed, update, 0)  # Start the update timer
glutMainLoop()