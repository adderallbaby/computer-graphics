import math
from OpenGL.GLUT import *
from OpenGL.GL import *

solidness = 0
l = 0.75
a = math.pi
m2 = (1, 0, -l * math.cos(a), 0,
0, 1, -l * math.sin(a), 0,
1, 0, -1, 0,
0, 0, 0, 1)
T=(1, 0, 0, 0 ,
0, 1, 0, 0,
math.cos(a), math.sin(a), -1, 0,
0, 0, 0, 1)
size = 1

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)


def display():
    glLoadIdentity()

    n = (1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         1, -1, -3, 1)
    glMultMatrixd(n)
    glClear(GL_COLOR_BUFFER_BIT)

    glMultMatrixd(T)

    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)
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
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glColor3f(0.0, 1.0, 1.0)
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



    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)
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
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glColor3f(0.0, 1.0, 1.0)
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
    global a, b, T, solidness, l
    if key == b'1':
        a += math.pi / 12
        l +=0.75
        T = (1, 0, 0, 0,
             0, 1, 0, 0,
             math.cos(a), math.sin(a), -1, 0,
             0, 0, 0, 1)
    if key == b'2':
        a -= math.pi / 12

        l += 0.75
        a = math.pi

        T = (1, 0, 0, 0,
             0, 1, 0, 0,
             math.cos(a), math.sin(a), -1, 0,
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
    glutInitWindowPosition(100, 100)
    glutCreateWindow('cube')
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMainLoop()


if __name__ == "__main__":
    main()
