from OpenGL.GL import *
from OpenGL.GLUT import *

import random


W_Width, W_Height = 500, 800

bullet = []
score = 0
misfires = 0
freeze = False
gameover = 0
special_bubble = None  # To handle the special circle functionality
special_bubble_timer = 0  # Timer for radius expansion and shrinking
expand = True  # To control expansion and shrinking

###################################################################
class Bubble:
    def __init__(self):
        self.x = random.randint(-220, 220)
        self.y = 330
        self.r = random.randint(20, 25)
        self.color = [1, 1, 0]

class SpecialBubble(Bubble):
    def __init__(self):
        super().__init__()
        self.r = random.randint(15, 20)
        self.color = [0, 1, 0]  # Green

class Catcher:
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]

###################################### Mid-Point Line Drawing Algorithm
def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def convert_from_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)

    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, zone)
    plot_point(x0, y0)

    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = convert_from_zone0(x, y, zone)
        plot_point(x0, y0)

########### Mid-Point Circle Drawing Algorithm

def midpointcircle(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, -y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()

##################################################################

bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
bubble.sort(key=lambda b: b.x)
catcher = Catcher()

###################################################################
def draw_bullet():
    global bullet
    glPointSize(2)
    glColor3f(1, 1, 1)
    for i in bullet:
        midpointcircle(8, i[0], i[1])

####################################################################
def draw_bubble():
    global bubble, special_bubble
    glPointSize(2)

    for i in range(len(bubble)):
        if i == 0:
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpointcircle(bubble[i].r, bubble[i].x, bubble[i].y)
        elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpointcircle(bubble[i].r, bubble[i].x, bubble[i].y)

    # Draw the special bubble
    if special_bubble:
        glColor3f(special_bubble.color[0], special_bubble.color[1], special_bubble.color[2])
        midpointcircle(special_bubble.r, special_bubble.x, special_bubble.y)

###############################################################################
def draw_ui():
    global catcher

    # Shooter (Triangle-shaped spaceship)
    glPointSize(2)
    glColor3f(catcher.color[0], catcher.color[1], catcher.color[2])

    # Define triangle points relative to catcher.x and base position -365
    base_x = catcher.x
    base_y = -365
    triangle_points = [
        (base_x, base_y + 20),      # Top point of the triangle
        (base_x - 15, base_y - 10), # Bottom-left point of the triangle
        (base_x + 15, base_y - 10), # Bottom-right point of the triangle
    ]

    # Draw triangle using points
    for i in range(len(triangle_points)):
        start_point = triangle_points[i]
        end_point = triangle_points[(i + 1) % len(triangle_points)]  # Loop to connect last to first
        midpoint_line(start_point[0], start_point[1], end_point[0], end_point[1])

    # Left button
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_line(-208, 350, -160, 350)
    glPointSize(3)
    midpoint_line(-210, 350, -190, 370)
    midpoint_line(-210, 350, -190, 330)

    # Right Cross Button
    glPointSize(4)
    glColor3f(0.9, 0, 0)
    midpoint_line(210, 365, 180, 335)
    midpoint_line(210, 335, 180, 365)

    # Middle Pause Button
    glPointSize(4)
    glColor3f(1, .5, 0)
    if freeze:
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else:
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)

#####################################################################
def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b

#######################################################################
def keyboardListener(key, x, y):
    global bullet, freeze, gameover, catcher
    if key == b' ':
        if not freeze and gameover < 3:
            bullet.append([catcher.x, -365])
    elif key == b'a':
        if catcher.x > -230 and not freeze:
            catcher.x -= 10
    elif key == b'd':
        if catcher.x < 230 and not freeze:
            catcher.x += 10
    glutPostRedisplay()

#########################################################################
def mouseListener(button, state, x, y):
    global freeze, gameover, catcher, score, bubble, bullet, misfires
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            freeze = False
            print('Starting Over')
            bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
            bubble.sort(key=lambda b: b.x)
            score = 0
            gameover = 0
            misfires = 0
            bullet = []

        if 170 < c_x < 216 and 330 < c_y < 370:
            print('Goodbye! Score:', score)
            glutLeaveMainLoop()

        if -25 < c_x < 25 and 325 < c_y < 375:
            freeze = not freeze

    glutPostRedisplay()

#############################################################
# Function to render text on screen
def render_text(x, y, text, color=(1, 1, 1)):
    glColor3f(color[0], color[1], color[2])
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Modify the display function to show "Game Over" when the game ends
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_ui()
    draw_bullet()
    draw_bubble()

    # Show Game Over message if the game is over
    if gameover >= 3 or misfires >= 3:
        render_text(-40, 50, "Game Over!", color=(1, 0, 0))  # Red color for Game Over

    glutSwapBuffers()

################################################################################
import time
def animate():
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = current_time

    global freeze, bubble, catcher, gameover, score, bullet, misfires, special_bubble, special_bubble_timer, expand
    if not freeze and gameover < 3 and misfires < 3:
        delidx = []
        for i in range(len(bullet)):
            if bullet[i][1] < 400:
                bullet[i][1] += 10
            else:
                delidx.append(i)
                misfires += 1
        try:
            for j in delidx:
                del bullet[j]
        except:
            pass

        for i in range(len(bubble)):
            if i == 0:
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble())
                    bubble.sort(key=lambda b: b.y)
            elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                    abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble())
                    bubble.sort(key=lambda b: b.y)

        # Handle special bubble creation and animation
        if not special_bubble and random.random() < 0.01:
            special_bubble = SpecialBubble()
        
        if special_bubble:
            if special_bubble.y > -400:
                special_bubble.y -= (10 + score * 5) * delta_time

                # Expand and shrink radius
                if expand:
                    special_bubble.r += 0.2
                    if special_bubble.r >= 30:
                        expand = False
                else:
                    special_bubble.r -= 0.2
                    if special_bubble.r <= 15:
                        expand = True
            else:
                special_bubble = None
                gameover += 1  # Increment gameover when the special bubble crosses the boundary

        try:
            for i in range(len(bubble)):
                # Check collision with shooter
                if abs(bubble[i].y - -345) < (bubble[i].r) and abs(bubble[i].x - catcher.x) < (bubble[i].r + 20):
                    gameover += 3  # Game over
                for j in range(len(bullet)):
                    if abs(bubble[i].y - bullet[j][1]) < (bubble[i].r + 15) and abs(bubble[i].x - bullet[j][0]) < (
                            bubble[i].r + 20):
                        score += 1
                        print("Score:", score)
                        del bubble[i]
                        del bullet[j]
                        bubble.append(Bubble())

            if special_bubble:
                # Check collision with shooter
                if abs(special_bubble.y - -345) < (special_bubble.r) and abs(special_bubble.x - catcher.x) < (special_bubble.r + 20):
                    gameover += 3
                for j in range(len(bullet)):
                    if abs(special_bubble.y - bullet[j][1]) < (special_bubble.r + 15) and abs(special_bubble.x - bullet[j][0]) < (
                            special_bubble.r + 20):
                        score += 3
                        print("Special Hit! Score:", score)
                        special_bubble = None
                        del bullet[j]
                        break

        except:
            pass

    if (gameover >= 3 or misfires >= 3) and not freeze:
        print("Game Over! Score:", score)
        freeze = True
        bubble = []  # Bubbles vanish
        special_bubble = None

    time.sleep(1 / 1000)
    glutPostRedisplay()


################################################################################

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -400, 400, -1, 1)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Shoot The Circles!")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
