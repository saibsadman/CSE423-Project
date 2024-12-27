from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_COLS = WINDOW_WIDTH // GRID_SIZE
GRID_ROWS = WINDOW_HEIGHT // GRID_SIZE

# These are the Game variables
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
countdown = 3  
start_time = time.time()  
speed = 200  # Initially the  snake speed in milliseconds
OBSTACLE_COUNT = 3
obstacles = []

first_portal = None
second_portal = None
portal_running = False
timer_for_portal = None


SNAKE_COLOR = (0.0, 0.8, 0.0) 
FOOD_COLOR = (1.0, 0.0, 0.0)   
POISONOUS_FOOD_COLOR = (0.0, 0.0, 1.0)  
SHELL_COLOR = (1.0, 1.0, 0.0) 
SCORE_COLOR = (1.0, 1.0, 1.0) 

# snake segment using gl_points
def draw_segment(x, y, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    center_x = x * GRID_SIZE + GRID_SIZE / 2
    center_y = y * GRID_SIZE + GRID_SIZE / 2
    radius = GRID_SIZE / 2
    for i in range(-int(radius), int(radius) + 1):
        for j in range(-int(radius), int(radius) + 1):
            if i**2 + j**2 <= radius**2:  
                glVertex2f(center_x + i, center_y + j)
    glEnd()

# Food drawing
def draw_food(x, y, color):
    glColor3f(*color)
    glBegin(GL_POINTS)
    start_x = x * GRID_SIZE
    start_y = y * GRID_SIZE
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            glVertex2f(start_x + i, start_y + j)
    glEnd()

#Midpoint line drawing
def draw_line(x0, y0, x1, y1, color=(1.0, 0.0, 0.0)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    
    # Identify the line's zone
    dx = x1 - x0
    dy = y1 - y0

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

    # Midpoint algorithm in Zone 0
    dx = x1_zone - x0_zone
    dy = y1_zone - y0_zone
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)

    x, y = x0_zone, y0_zone
    while x <= x1_zone:
        orig_x, orig_y = from_zone0(x, y, zone)
        glVertex2f(orig_x, orig_y)
        if d <= 0:
            d += incrE
        else:
            d += incrNE
            y += 1
        x += 1

    glEnd()


#Obstacle Drawing
def draw_obstacle(x, y, size, color=(1.0, 0.0, 0.0)):  
    half_size = size // 2
    draw_line(x - half_size, y - half_size, x + half_size, y - half_size, color)  
    draw_line(x - half_size, y - half_size, x, y + half_size, color)  
    draw_line(x, y + half_size, x + half_size, y - half_size, color)  


# Shell drawing
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

#Teleportation portals
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
    ("Game Rules:", (1.0, 1.0, 0.0)),  
    ("1. Catch the Red foods", (1.0, 0.0, 0.0)),  
    ("2. Beware of the Blue poisonous food", (0.0, 0.0, 1.0)),  
    ("3. Catch the yellow shell to get back to original shape", (0.0, 1.0, 0.0)),  
    ("4. Speed increases upon scoring 80 points", (0.0, 1.0, 1.0)),
    ("5. Use Teleportation portals to teleport from one location to another", (0.5, 0.8, 0.2)),
    ("6. Avoid the obstacles", (1.0, 0.6, 1.0))
]

#obstacle generation
def generate_obstacles():
    global obstacles
    obstacles = [{'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)} for i in range(3)]

# teleportation portals generation
def portal_generation():
    global first_portal, second_portal, portal_running, timer_for_portal
    first_portal = {'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)}
    second_portal = {'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)}
    portal_running = True
    timer_for_portal = time.time()


# Checking if the snake collides with any obstacles
def check_obstacle_collision():
    global game_over, first_portal, second_portal, portal_running
    head = snake[0]
    for obstacle in obstacles:
        if head['x'] == obstacle['x'] and head['y'] == obstacle['y']:
            game_over = True
            first_portal = None
            second_portal = None
            portal_running = False
            print(f"Game Over! Collided with an obstacle. Final Score: {score}")

            
def display():
    global game_over, shell, shell_active, startup_phase, countdown, start_time, obstacles
    glClear(GL_COLOR_BUFFER_BIT)

    if startup_phase:
        for i, (message, color) in enumerate(startup_messages):
            render_text(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2 - (i * 30), message, color)
        if time.time() - start_time > 5:  # 5 seconds for "Beware" message
            startup_phase = False
            countdown = 3  
            start_time = time.time()  # Reset the start time for countdown
    elif countdown > 0:
        render_text(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2, f"Game will start in {countdown}...", SCORE_COLOR)
        if time.time() - start_time > 1:  
            countdown -= 1
            start_time = time.time()  
    else:
        if not game_over:
            for segment in snake: # Draw the snake
                draw_segment(segment['x'], segment['y'], SNAKE_COLOR)

            draw_food(food['x'], food['y'], FOOD_COLOR) ## Draw the food

            if poisonous_food:  # Draw the poisonous food if it exists
                draw_food(poisonous_food['x'], poisonous_food['y'], POISONOUS_FOOD_COLOR)

            if shell: # Draw the shell 
                draw_circle(shell['x'] * GRID_SIZE + GRID_SIZE / 2, shell['y'] * GRID_SIZE + GRID_SIZE / 2, GRID_SIZE, SHELL_COLOR)
            
            for obstacle in obstacles:
                draw_obstacle(obstacle['x'] * GRID_SIZE + GRID_SIZE // 2, obstacle['y'] * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE, (1.0, 0.0, 0.0)) 
            if portal_running: # Draw the teleportation portal
                draw_teleportation()


            # Score display
            render_text(10, WINDOW_HEIGHT - 20, f"Score: {score}", SCORE_COLOR)
            render_text(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 20, "Press P: Pause/Resume", SCORE_COLOR)
        else:
            render_text(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2, "Game Over!", SCORE_COLOR)
            render_text(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2 - 40, "Press R to Restart", SCORE_COLOR)
    glutSwapBuffers()

# Move the snake
def move_snake():
    global snake, food, poisonous_food, poisonous_food_timer, shell, shell_active, shell_timer
    global direction, game_over, score, food_count, poisonous_food_eaten, paused, startup_phase, speed
    global first_portal, second_portal, portal_running  

    if game_over or paused or startup_phase:
        return

    head = snake[0].copy()
    if direction == 'UP':
        head['y'] += 1
    elif direction == 'DOWN':
        head['y'] -= 1
    elif direction == 'LEFT':
        head['x'] -= 1
    elif direction == 'RIGHT':
        head['x'] += 1

    # Wall collision checking
    if head['x'] < 0 or head['x'] >= GRID_COLS or head['y'] < 0 or head['y'] >= GRID_ROWS:
        game_over = True
        first_portal = None
        second_portal = None
        portal_running = False
        print(f"Game Over! Final Score: {score}")
        return

    # Check for self-collision
    if head in snake:
        game_over = True
        first_portal = None
        second_portal = None
        portal_running = False
        print(f"Game Over! Final Score: {score}")
        return
    
    snake.insert(0, head) #snake moving by adding new head

    # Check for food eating
    if head['x'] == food['x'] and head['y'] == food['y']:
        food['x'] = random.randint(0, GRID_COLS - 1)
        food['y'] = random.randint(0, GRID_ROWS - 1)
        score += 10
        food_count += 1
        generate_obstacles()

        # Adjusting speed every 80 points
        if score % 80 == 0:
            speed = max(50, speed - 100)  # Reduce time for moving the snake but not below 50ms


        # Reset poisonous food whenever normal food is eaten
        poisonous_food = None
        poisonous_food_timer = None

        if food_count % 3 == 0: #generating poisonous food
            poisonous_food = {'x': random.randint(0, GRID_COLS - 1), 'y': random.randint(0, GRID_ROWS - 1)}
            poisonous_food_timer = time.time()

        if food_count % 8 == 0 and not shell_active:
            shell_x = random.randint(0 + (GRID_SIZE // 2), GRID_COLS - 1 - (GRID_SIZE // 2))
            shell_y = random.randint(0 + (GRID_SIZE // 2), GRID_ROWS - 1 - (GRID_SIZE // 2))
            shell = {'x': shell_x, 'y': shell_y}
            shell_active = True
            shell_timer = time.time() 

    else:
        snake.pop()
    check_obstacle_collision()

    if shell:
        head_x = head['x'] * GRID_SIZE + GRID_SIZE / 2  
        head_y = head['y'] * GRID_SIZE + GRID_SIZE / 2
        shell_x = shell['x'] * GRID_SIZE + GRID_SIZE / 2
        shell_y = shell['y'] * GRID_SIZE + GRID_SIZE / 2
        distance = ((head_x - shell_x) ** 2 + (head_y - shell_y) ** 2) ** 0.5
        if distance <= GRID_SIZE:  
            snake = [snake[0]]  # Shrink snake to a single segment
            shell_active = False  
            shell = None 
            food_count = 0  
            score += 5
            shell_timer = None 

    if shell and time.time() - shell_timer > 10: #  # Check if the shell has expired 
        shell_active = False 
        shell = None 

    # Check if the snake eats the poisonous food
    if poisonous_food and head['x'] == poisonous_food['x'] and head['y'] == poisonous_food['y']:
        game_over = True
        print(f"Game Over! Final Score: {score}")
        poisonous_food_eaten = True
    
    if portal_running:
        if head['x'] == first_portal['x'] and head['y'] == first_portal['y']:
            snake[0] = second_portal  # Teleport snake head to portal B
        elif head['x'] == second_portal['x'] and head['y'] == second_portal['y']:
            snake[0] = first_portal  # Teleport snake head to portal A
  
    if portal_running and time.time() - timer_for_portal > 10: #teleportation portal will be available for 10 sec
        first_portal = None
        second_portal = None
        portal_running = False

def keyboard(key, x, y):
    global direction, game_over, paused, portal_running, first_portal, second_portal, timer_for_portal

    if game_over and key == b'r':  
        restart_game()
    elif key == b'p':  
        paused = not paused
    elif key == b' ':  
        if not portal_running: 
            portal_generation()  
            timer_for_portal = time.time()  
        else:
            first_portal = None 
            second_portal = None
            portal_running = False

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
    countdown = 3 
    start_time = time.time()  
    speed = 200 
    

def update(value):
    move_snake()
    glutPostRedisplay()
    glutTimerFunc(speed, update, 0) 


def initialize():
    glClearColor(0.0, 0.0, 0.0, 1.0) 
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1) 
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow(b"Snake Game with Shell and Poisonous Food")
initialize()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_input)
glutTimerFunc(speed, update, 0)
glutMainLoop()