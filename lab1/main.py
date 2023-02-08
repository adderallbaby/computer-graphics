from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

px = 300
py = 300
px2 = 300
py2 = 300
px3 = 300
py3 = 300
px4 = 300
py4 = 300

def drawPlayer():
    glColor3f(1,1,0)
    glPointSize(50)
    glBegin(GL_LINES)
    glVertex2i(px,py)
    glVertex2i(px+50,py+50)
    glEnd()
    glBegin(GL_LINES)
    glVertex2i(px, py)
    glVertex2i(px - 40, py - 10)
    glEnd()


    glBegin(GL_LINES)
    glVertex2i(px2,py2)
    glVertex2i(px2+50,py2+50)
    glEnd()
    glBegin(GL_LINES)
    glVertex2i(px2, py2)
    glVertex2i(px2 - 40, py2 - 10)
    glEnd()


    glBegin(GL_LINES)
    glVertex2i(px3,py3)
    glVertex2i(px3+50,py3+50)
    glEnd()
    glBegin(GL_LINES)
    glVertex2i(px3, py3)
    glVertex2i(px3 - 40, py3 - 10)
    glEnd()


    glBegin(GL_LINES)
    glVertex2i(px4,py4)
    glVertex2i(px4+50,py4+50)
    glEnd()
    glBegin(GL_LINES)
    glVertex2i(px4, py4)
    glVertex2i(px4 - 40, py4 - 10)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    drawPlayer()
    glutSwapBuffers()

# Here is my keyboard input code
def buttons(key,x,y):
    global px, py, px2,py3,py4
    if key == b'a':
        px -= 50
    if key == b'd':
        px2 += 50
    if key == b'w':
        py3 -= 50
    if key == b's':
        py4 += 50
    glutPostRedisplay()

def init():
    glClearColor(0.3,0.3,0.3,0)
    gluOrtho2D(0,1024,512,0)
    global px, py
    px = 300; py = 300

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1024, 512)
    window = glutCreateWindow("python")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(buttons)
    glutMainLoop()

if __name__ == "__main__":
    main()
