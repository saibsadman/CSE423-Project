from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time


W_WIDTH, W_HEIGHT = 500, 790
bullet = [] # bullet er position track korar jonno
score = 0
misfires = 0
freeze = False
gameover = 0
unique_circle = None  
unique_circle_timer = 0 
expand = True  

class Bubble:
    def __init__(self):
        self.x = random.randint(-220, 220) #Random x position range er vitore
        self.y = 330 
        self.r = random.randint(20, 25)
        self.color = [1, 1, 0]

class UniqueCircle(Bubble):
    def __init__(self):
        super().__init__()
        self.r = random.randint(15, 20)
        self.color = [0, 1, 0]  

class Catcher: # spaceship
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]

def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def to_zone0(x, y, zone):
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

def from_zone0(x, y, zone):
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

    x1, y1 = to_zone0(x1, y1, zone)
    x2, y2 = to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incrEast = 2 * dy
    incrNorthEast = 2 * (dy - dx)

    x, y = x1, y1
    x0, y0 = from_zone0(x, y, zone)
    plot_point(x0, y0)

    while x < x2:
        if d <= 0:
            d += incrEast
            x += 1
        else:
            d += incrNorthEast
            x += 1
            y += 1
        x0, y0 = from_zone0(x, y, zone)
        plot_point(x0, y0)


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

bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble(), Bubble()] # Initializes six Bubble objects
bubble.sort(key=lambda b: b.x) # sorts them by their x position for placement.
catcher = Catcher()

def draw_bullet(): #bullet draw ekhane hoi
    global bullet # bullet list theke use kore
    glPointSize(2)
    glColor3f(1, 1, 1)
    for i in bullet:
        midpointcircle(8, i[0], i[1]) # radius=8, i[0] (x-coordinate) and i[1] (y-coordinate)

def draw_bubble(): # midpointcircle use kore regular and unique circle draw
    global bubble, unique_circle 
    glPointSize(2)

    for i in range(len(bubble)): 
        if i == 0: # The first bubble (index 0) is drawn
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2]) #sets the RGB color
            midpointcircle(bubble[i].r, bubble[i].x, bubble[i].y) #circle draw
        elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (   #Ensures that the current bubble (bubble[i]) is drawn only if it doesn’t overlap vertically with the previous bubble (bubble[i - 1]).
                abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)): #Ensures sufficient horizontal space between bubble[i] and bubble[i - 1].
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpointcircle(bubble[i].r, bubble[i].x, bubble[i].y)


    if unique_circle:
        glColor3f(unique_circle.color[0], unique_circle.color[1], unique_circle.color[2])
        midpointcircle(unique_circle.r, unique_circle.x, unique_circle.y)

def draw_ui():
    global catcher
    glPointSize(2)


    base_x = catcher.x # position of the catcher
    base_y = -365 #Vertical position, fixed

    glColor3f(1, 1, 0)  

    # Draw triangular tip
    midpoint_line(base_x, base_y + 60, base_x - 15, base_y + 40)  
    midpoint_line(base_x, base_y + 60, base_x + 15, base_y + 40)  
    midpoint_line(base_x - 15, base_y + 40, base_x + 15, base_y + 40) 
    # Draw the rectangular body
    midpoint_line(base_x - 10, base_y + 40, base_x - 10, base_y - 10)  
    midpoint_line(base_x + 10, base_y + 40, base_x + 10, base_y - 10)  
    midpoint_line(base_x - 10, base_y - 10, base_x + 10, base_y - 10)  

    # Draw fins
    midpoint_line(base_x - 10, base_y - 10, base_x - 20, base_y - 30)  
    midpoint_line(base_x + 10, base_y - 10, base_x + 20, base_y - 30)  
    # Draw exhaust pipes
    midpoint_line(base_x - 5, base_y - 30, base_x - 5, base_y - 40)  
    midpoint_line(base_x, base_y - 30, base_x, base_y - 40) 
    midpoint_line(base_x + 5, base_y - 30, base_x + 5, base_y - 40)  

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
    if freeze: # play icon
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else: # pauseicon
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)

    
    render_text(-240, 310, f"Score: {score}", color=(1, 1, 1))    
    render_text(-240, 290, f"Misfires: {misfires}", color=(1, 0, 0))  
    render_text(-240, 270, f"Missed: {gameover}", color=(1, 1, 0))  



def convert_coordinate(x, y): # alternative coordinate system (where the origin (0,0) is at the center of the screen)
    global W_WIDTH, W_HEIGHT
    a = x - (W_WIDTH / 2)
    b = (W_HEIGHT / 2) - y
    return a, b


def keyboardListener(key, x, y):
    global bullet, freeze, gameover, catcher
    if key == b' ':
        if not freeze and gameover < 3:
            bullet.append([catcher.x, -365 + 60]) #adds a new bullet to the bullet list
    elif key == b'a':
        if catcher.x > -230 and not freeze:
            catcher.x -= 10 # moving the catcher left by decreasing its x-coordinate by 10 pixel
    elif key == b'd':
        if catcher.x < 230 and not freeze:
            catcher.x += 10
    glutPostRedisplay()

def mouseListener(button, state, x, y): #restart, pause and game cancel er kaaj ekhane hoi
    global freeze, gameover, catcher, score, bubble, bullet, misfires
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            freeze = False
            print('Starting Over the game')
            bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
            bubble.sort(key=lambda b: b.x)
            score = 0
            gameover = 0
            misfires = 0
            bullet = []

        if 170 < c_x < 216 and 330 < c_y < 370:
            print('Goodbye! Final Score:', score)
            glutLeaveMainLoop()

        if -25 < c_x < 25 and 325 < c_y < 375:
            freeze = not freeze

    glutPostRedisplay()


def render_text(x, y, text, color=(1, 1, 1)):
    glColor3f(color[0], color[1], color[2])
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_ui()
    draw_bullet()
    draw_bubble()

  
    if gameover >= 3 or misfires >= 3: #gameover er condition
        render_text(-40, 50, "Game Over!", color=(1, 0, 0))  

    glutSwapBuffers()



def animate(): #game state update korar jonno
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0 # smooth animation er jonno
    animate.start_time = current_time #Stores the time of the last animation update.

    global freeze, bubble, catcher, gameover, score, bullet, misfires, unique_circle, unique_circle_timer, expand
    if not freeze and gameover < 3 and misfires < 3:
        delidx = []
        for i in range(len(bullet)):
            if bullet[i][1] < 400:
                bullet[i][1] += 10  #Bullet Movement
            else:
                delidx.append(i)
                misfires += 1
        try:
            for j in delidx:
                del bullet[j] #bullet delete
        except:
            pass

        for i in range(len(bubble)):
            if i == 0:
                if bubble[i].y > -400: # bubble within the game boundary
                    bubble[i].y -= (10 + score * 5) * delta_time # buble er downword movement and the speed of movement increases with the player's score (scaled by score * 5)
                else:
                    gameover += 1 #boundary cross kora
                    del bubble[i] # Removes the bubble from the bubble list jehetu ata boundary cross kore felse
                    bubble.append(Bubble()) # Creates a new Bubble object to replace the one that was removed. 
                    bubble.sort(key=lambda b: b.y)
            elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (  # Ensures that there is enough vertical space between the current bubble and the previous bubble (bubble[i - 1])
                    abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble())
                    bubble.sort(key=lambda b: b.y)


        if not unique_circle and random.random() < 0.01: #a special bubble
            unique_circle = UniqueCircle() # create a new UniqueCircle.
        
        if unique_circle:
            if unique_circle.y > -400:
                unique_circle.y -= (10 + score * 5) * delta_time # Moves the unique_circle down the screen and also speed increase

                if expand:
                    unique_circle.r += 0.2 # Animates the unique_circle to gradually expand r by 0.2 per frame.
                    if unique_circle.r >= 30: # r 30 reach korar pore expand korbena
                        expand = False
                else:
                    unique_circle.r -= 0.2 # shrink shart
                    if unique_circle.r <= 15:
                        expand = True
            else:
                unique_circle = None # unique_circle has moved out of boundary
                gameover += 1  

        try:
            for i in range(len(bubble)):
                spaceship_points = [ # These points will be used to detect collisions with circles.
                    (catcher.x, -365 + 60),
                    (catcher.x - 10, -365 + 40),
                    (catcher.x + 10, -365 + 40), 
                    (catcher.x - 10, -365 - 10), 
                    (catcher.x + 10, -365 - 10), 
                    (catcher.x - 20, -365 - 30), 
                    (catcher.x + 20, -365 - 30), 
                ]
                
                for point in spaceship_points:  # A collision detect korar jonno spaceship er sathe
                    if abs(bubble[i].x - point[0]) < bubble[i].r and abs(bubble[i].y - point[1]) < bubble[i].r: #
                        gameover += 3 
                        break
                
                for j in range(len(bullet)): #  Detects if a bullet hits a bubble.
                    if abs(bubble[i].y - bullet[j][1]) < (bubble[i].r + 15) and abs(bubble[i].x - bullet[j][0]) < (bubble[i].r + 20): # A hit is detected if the distance between the bullet and the bubble's center is less than their combined effective radius 
                        score += 1
                        print("Score:", score)
                        del bubble[i]
                        del bullet[j]
                        bubble.append(Bubble())

            if unique_circle:
                for point in spaceship_points: #unique circle er jonno spaceship er sathe collusion
                    if abs(unique_circle.x - point[0]) < unique_circle.r and abs(unique_circle.y - point[1]) < unique_circle.r:
                        gameover += 3  
                        break

                for j in range(len(bullet)): #unique circle er bullet er detection
                    if abs(unique_circle.y - bullet[j][1]) < (unique_circle.r + 15) and abs(unique_circle.x - bullet[j][0]) < (
                            unique_circle.r + 20):
                        score += 3
                        print("Special Hit! Score:", score)
                        unique_circle = None
                        del bullet[j]
                        break

        except:
            pass

    if (gameover >= 3 or misfires >= 3) and not freeze: #game over er condition
        print("Game Over! Score:", score)
        freeze = True
        bubble = [] 
        unique_circle = []

    time.sleep(1 / 1000) #tiny delay to ensure the game loop doesn’t run too fast. 
    glutPostRedisplay()
def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -400, 400, -1, 1)


glutInit()
glutInitWindowSize(W_WIDTH, W_HEIGHT)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Shoot The Circles Game!")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
