# Task 1

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_WIDTH, W_HEIGHT = 500, 500

raining_drops = []
bg_color = 0.0
bending = 0.0        
max_bending = 1.0

def init_rain(count):
    global raining_drops
    raining_drops = []
    for i in range(count):
        drop = {'x': random.randint(0, W_WIDTH), 'y': random.randint(0, W_HEIGHT)}
        raining_drops.append(drop)

#House Base
def draw_house():
    glColor3f(1.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(150, 100)
    glVertex2f(350, 100)
    glVertex2f(350, 100)
    glVertex2f(350, 250)
    glVertex2f(350, 250)
    glVertex2f(150, 250)
    glVertex2f(150, 250)
    glVertex2f(150, 100)
    glEnd()

    # Roof Drawing
    glColor3f(0.5, 0.6, 0.2)  # Dark gray for the roof
    glBegin(GL_TRIANGLES)
    glVertex2f(130, 250)
    glVertex2f(370, 250)
    glVertex2f(250, 350)
    glEnd()

    # Door
    glColor3f(1.0, 0.85, 0.0)  # Light gray for the door
    glBegin(GL_LINES)
    glVertex2f(220, 100)
    glVertex2f(220, 180)
    glVertex2f(220, 180)
    glVertex2f(260, 180)
    glVertex2f(260, 180)
    glVertex2f(260, 100)
    glEnd()

    #Door knob
    glColor3f(1.0, 0.6, 0.9)
    glPointSize(3) 
    glBegin(GL_POINTS)
    glVertex2f(250,140)
    glEnd()

    # window
    glColor3f(0.5, 0.6, 0.2)
    glBegin(GL_LINES)
    glVertex2f(280, 190)
    glVertex2f(320, 190)
    glVertex2f(320, 190)
    glVertex2f(320, 230)
    glVertex2f(320, 230)
    glVertex2f(280, 230)
    glVertex2f(280, 230)
    glVertex2f(280, 190)
    glVertex2f(300, 190)
    glVertex2f(300, 230)
    glVertex2f(280, 210)
    glVertex2f(320, 210)
    glEnd()


def rain_drawing():
    glColor3f(0.5, 0.3, 0.9) 
    glBegin(GL_LINES)
    for drop in raining_drops:
        glVertex2f(drop['x'], drop['y'])                            
        glVertex2f(drop['x'] + bending * 10, drop['y'] - 10)      
    glEnd()

def update_rain_drops():
    for drop in raining_drops:
        drop['x'] += bending  
        drop['y'] -= 5         

        if drop['y'] < 0:
            drop['y'] = W_HEIGHT
            drop['x'] = random.randint(0, W_WIDTH)

        if drop['x'] < 0:
            drop['x'] = W_WIDTH
        elif drop['x'] > W_WIDTH:
            drop['x'] = 0

    glutPostRedisplay()


def bg_changing(step):
    global bg_color
    bg_color = max(0.0, min(1.0, bg_color + step))  
    glClearColor(bg_color, bg_color, bg_color, 1.0)  

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_house()
    rain_drawing()
    glutSwapBuffers()

def specialKeyListener(key, x, y):
    global bending
    if key == GLUT_KEY_LEFT:
        bending = max(-max_bending, bending - 0.1)
    elif key == GLUT_KEY_RIGHT:
        bending = min(max_bending, bending + 0.1)
    elif key == GLUT_KEY_F1:  
        bg_changing(0.06)
    elif key == GLUT_KEY_F2: 
        bg_changing(-0.06)
    
    glutPostRedisplay()

def iterate():
    glViewport(0, 0, W_WIDTH, W_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_WIDTH, 0.0, W_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W_WIDTH, W_HEIGHT)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"House with Rain")
glClearColor(bg_color, bg_color, bg_color, 1.0) 
glPointSize(5) 

init_rain(50)
glutDisplayFunc(show_screen)
glutIdleFunc(update_rain_drops)
glutSpecialFunc(specialKeyListener)
iterate()
glutMainLoop()






# Task 2

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random
# import time

# W_WIDTH, W_HEIGHT = 500, 500
# Size_of_point = 5
# Boundary = 10

# #Below are global variables
# points = []
# speed = 0.1
# frozen_status = False
# last_blink_time = time.time()
# blink_state = True

# def draw_point(x, y, color):
#     glColor3f(*color)
#     glPointSize(Size_of_point)
#     glBegin(GL_POINTS)
#     glVertex2f(x, y)
#     glEnd()

# def update():
#     global points, speed, frozen_status, blink_state, last_blink_time

#     if frozen_status:
#         return

#     current_time = time.time()
#     if current_time - last_blink_time > 0.1:  # Blinking will happen in every 0.1 sec
#         blink_state = not blink_state
#         last_blink_time = current_time

#     for position in points:
#         position["x"] += position["dx"] * speed
#         position["y"] += position["dy"] * speed

#         # Bouncing of the wall will happen here
#         if position["x"] < Boundary or position["x"] > W_WIDTH - Boundary:
#             position["dx"] *= -1
#         if position["y"] < Boundary or position["y"] > W_HEIGHT - Boundary:
#             position["dy"] *= -1

#     glutPostRedisplay()

# def display():
#     global points, blink_state
#     glClear(GL_COLOR_BUFFER_BIT)

#     for position in points:
#         if position.get("blink", False):
#             color = position["color"] if blink_state else (0, 0, 0) #black color
#         else:
#             color = position["color"] #real color
#         draw_point(position["x"], position["y"], color)

#     glutSwapBuffers()

# def keyboard_listener(key, x, y):
#     global frozen_status
#     key = key.decode("utf-8")
#     if key == "\x1b":  
#         glutLeaveMainLoop()
#     elif key == " ": 
#         frozen_status = not frozen_status
#         print("Frozen" if frozen_status else "Unfrozen")

#     glutPostRedisplay()

# def special_key_listener(key, x, y):
#     global speed

#     if key == GLUT_KEY_UP:  
#         speed *= 2
#         print("Speed Increased")
#     elif key == GLUT_KEY_DOWN:
#         speed /= 2
#         print("Speed Decreased")

#     glutPostRedisplay()

# def mouse_listener(button, state, x, y):
#     global points

#     if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
#         x_point = x
#         y_point = W_HEIGHT - y 
#         point = {
#             "x": x_point,
#             "y": y_point,
#             "dx": random.choice([-1, 1]),
#             "dy": random.choice([-1, 1]),
#             "color": (random.random(), random.random(), random.random()),
#             "blink": False 
#         }
#         points.append(point)
#     elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#         for point in points:
#             point["blink"] = not point.get("blink", False)
#         print("Blinking for all points")

#     glutPostRedisplay()



# glutInit()
# glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
# glutInitWindowSize(W_WIDTH, W_HEIGHT)
# glutCreateWindow(b"Building The Amazing Box")

# glClearColor(0, 0, 0, 0)  #background color black
# glMatrixMode(GL_PROJECTION)
# glLoadIdentity()
# glOrtho(0, W_WIDTH, 0, W_HEIGHT, -1, 1)
# glMatrixMode(GL_MODELVIEW)

# glutDisplayFunc(display)
# glutIdleFunc(update)
# glutKeyboardFunc(keyboard_listener)
# glutSpecialFunc(special_key_listener)
# glutMouseFunc(mouse_listener)
# glutMainLoop()




