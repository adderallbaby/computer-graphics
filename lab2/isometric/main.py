import math
from OpenGL.GLUT import *
from OpenGL.GL import *
from math import sin, cos

solidness = 0

a = math.pi

b = math.pi

size = 1

T = (cos(a), 0, sin(a), 0,
     sin(a) * cos(b), cos(b), -cos(a) * sin(b), 0,
     math.cos(b) * sin(a), -math.sin(a), -cos(a) * cos(b), 0,
     0, 0, 0, 1)


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)


def display():
    glLoadIdentity()

    n = (1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         -0.3, -0.5, -3, 1)

    glMultMatrixd(n)
    glClear(GL_COLOR_BUFFER_BIT)
    glMultMatrixd(T)

    if solidness == 0:
        glBegin(GL_LINES)
    if solidness == 1:
        glBegin(GL_QUADS)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)

    if solidness == 0:
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(size / 2, -size / 2, -size / 2)
        glVertex3f(size / 2, size / 2, -size / 2)
        glVertex3f(size / 2, size / 2, size / 2)
        glVertex3f(size / 2, -size / 2, size / 2)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glEnd()

    glLoadIdentity()
    n = (1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         1, 1, -3, 1)
    glMultMatrixd(n)

    if solidness == 0:
        glBegin(GL_LINES)
    if solidness == 1:
        glBegin(GL_QUADS)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)

    if solidness == 0:
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(size / 2, -size / 2, -size / 2)
        glVertex3f(size / 2, size / 2, -size / 2)
        glVertex3f(size / 2, size / 2, size / 2)
        glVertex3f(size / 2, -size / 2, size / 2)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()
    glFlush()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)

    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    glMatrixMode(GL_MODELVIEW)


def keyboard(key, x, y):
    global a, b, T, solidness
    if key == b'1':
        a += math.pi / 48
        a = a % math.pi + math.pi
        T = (cos(a), 0, sin(a), 0,
             sin(a) * cos(b), cos(b), -cos(a) * sin(b), 0,
             math.cos(b) * sin(a), -math.sin(a), -cos(a) * cos(b), 0,
             0, 0, 0, 1)
    if key == b'2':
        a -= math.pi / 48
        a = a % math.pi + math.pi

        T = (cos(a), 0, sin(a), 0,
             sin(a) * cos(b), cos(b), -cos(a) * sin(b), 0,
             math.cos(b) * sin(a), -math.sin(a), -cos(a) * cos(b), 0,
             0, 0, 0, 1)
    if key == b'3':
        solidness = 0
    if key == b'4':
        solidness = 1
    glutPostRedisplay()


def main():
    global a
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow('cube')
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMainLoop()


if __name__ == "__main__":
    main()
