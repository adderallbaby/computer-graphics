import math
from OpenGL.GLUT import *
from OpenGL.GL import *
import glfw
from OpenGL.raw.GLU import gluLookAt
from math import sin, cos
degree = 0.0
cnt = 10


'''
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()                         #перемещаем в центр СК
    glRotatef(degree * 50, 1, 0, 0)  # отвечает за поворот

    glScalef(0.6, 0.6, 1)                    # изменяем мастштаб


    l = 0.5
    a = math.pi * 2 / cnt

    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0, 0, 1)
    glVertex2f(0, 0)
    for i in range(-1, cnt):
        x = sin(a * i) * l
        y = cos(a * i ) * l
        glColor3f(0, i / 10.0, 1)
        glVertex2f(x, y)

    glEnd()

    #glPopMatrix()

'''



def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)




def display():
    glLoadIdentity()  # перемещаем в центр СК
    glRotatef(25, 0,2, 0)  # отвечает за поворот
    glClear(GL_COLOR_BUFFER_BIT)

    glScalef(0.6, 0.6, 0.5)  # изменяем мастштаб

    l = 0.5
    a = math.pi * 4 / cnt
    n = (1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         0, 0, 0, 1)

    glMultMatrixd(n)

    glLoadIdentity()

    glBegin(GL_TRIANGLE_STRIP)
    glColor3f(0, 0, 0)
    glVertex3f(0, 0,0)
    for i in range(-1, cnt):
        x = sin(a * i) * l
        y = cos(a * i) * l
        glColor3f(0, 11 / 10.0, 1)
        glVertex3f(x, y,0)


    glEnd()


    glLoadIdentity()
    glRotatef(25, 0,2, 0)  # отвечает за поворот

    glScalef(0.6, 0.6, 0.5)  # изменяем мастштаб

    l = 0.5
    a = math.pi * 4 / cnt
    n = (1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         0, 0, 0, 1)

    glMultMatrixd(n)
    glBegin(GL_TRIANGLE_STRIP)
    glColor3f(0, 0, 0)
    glVertex3f(0, 0, -1)
    for i in range(-1, cnt):
        x = sin(a * i) * l
        y = cos(a * i) * l
        glColor3f(0, 1 / 10.0, 1)
        glVertex3f(x, y,-1)

    glEnd()
    glVertex3f(0, 0,0)
    glBegin(GL_LINES)
    glColor3f(0, 0, 0)

    for i in range(-1, cnt):
        x = sin(a * i) * l
        y = cos(a * i) * l
        glColor3f(0, 11 / 10.0, 1)
        glVertex3f(x/0.6, y/0.6, 0)
        glVertex3f(x*0.6, y*0.6, -1*0.6)

    glEnd()
    glLoadIdentity()

    glFlush()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)

    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    glMatrixMode(GL_MODELVIEW)






def key(key, x, y) :
    global cnt
    global degree
    l = 0.5
    a = math.pi * 4 / cnt

    if (key == b'1'):
        cnt -= 2
    elif (key == b'2'):
        cnt += 2



    glutPostRedisplay()


def main():
    global a
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow('cube')
    init()
    glutDisplayFunc(display)
    #glutReshapeFunc(reshape)
    glutKeyboardFunc(key)
    glutMainLoop()


if __name__ == "__main__":
    main()
