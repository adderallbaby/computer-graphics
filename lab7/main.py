from math import *

import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *


def read_rows(path):
    image_file = open(path, "rb")
    # Blindly skip the BMP header.
    image_file.seek(54)

    # We need to read pixels in as rows to later swap the order
    # since BMP stores pixels starting at the bottom left.
    rows = []
    row = []
    pixel_index = 0

    while True:
        if pixel_index == 512:
            pixel_index = 0
            rows.insert(0, row)
            if len(row) != 512 * 3:
                raise Exception("Row length is not 1920*3 but " + str(len(row)) + " / 3.0 = " + str(len(row) / 3.0))
            row = []
        pixel_index += 1

        r_string = image_file.read(1)
        g_string = image_file.read(1)
        b_string = image_file.read(1)

        if len(r_string) == 0:
            # This is expected to happen when we've read everything.
            if len(rows) != 512:
                print(
                    "Warning!!! Read to the end of the file at the correct sub-pixel (red) but we've not read 1080 rows!"
                )
            break

        if len(g_string) == 0:
            print("Warning!!! Got 0 length string for green. Breaking.")
            break

        if len(b_string) == 0:
            print("Warning!!! Got 0 length string for blue. Breaking.")
            break

        r = ord(r_string)
        g = ord(g_string)
        b = ord(b_string)

        row.append(b)
        row.append(g)
        row.append(r)

    image_file.close()

    return rows


def repack_sub_pixels(rows):
    print("Repacking pixels...")
    sub_pixels = []
    for row in rows:
        for sub_pixel in row:
            sub_pixels.append(sub_pixel)

    diff = len(sub_pixels) - 512 * 512 * 3
    print("Packed", len(sub_pixels), "sub-pixels.")
    if diff != 0:
        print(
            "Error! Number of sub-pixels packed does not match 1920*1080: ("
            + str(len(sub_pixels))
            + " - 1920 * 1080 * 3 = "
            + str(diff)
            + ")."
        )

    return sub_pixels


"""

две функции выше отсюда взяты https://stackoverflow.com/questions/10439104/reading-bmp-files-in-python
просто считывают текстуру


"""
rows = read_rows("7.bmp")
image = repack_sub_pixels(rows)

sc = 0.1
x = 0
y = 0
z = 0
v0 = 0
g = 0.00051
surface = -2
h0 = 0
light = True
moving = False
it = False
texture = 0
light_position = [0., 0, 10.0, 1.0]
material_diffusion = [10, 10, 10, 1.0]
light_diffusion = [10, 10, 10]
Kl = 0.01
Kq = 0.002
Kc = 0.001
vertices = (
    # x  y  z
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfs = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)
colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
)


def drawFigure(x, y, z, angle1, angle2, angle3, s):
    glScalef(s, s, s)
    glEnable(GL_DEPTH_TEST)

    lines = False

    glTranslatef(x, y, z)
    glRotatef(angle1, 1, 0, 0)
    glRotatef(angle2, 0, 1, 0)
    glRotatef(angle3, 0, 0, 1)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    back = [[-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5]]
    tback = [[-0.5 + 0.27 * 2, -0.5 + 0.25 * 2], [-0.5 + 0.27 * 2, 0.5 + 0.25 * 2], [0.5 + 0.27 * 2, 0.5 + 0.25 * 2],
             [0.5 + 0.27 * 2, -0.5 + 0.25 * 2]]

    glEnableClientState(GL_VERTEX_ARRAY)
    glTexCoordPointer(2, GL_FLOAT, 0, tback)

    glVertexPointer(3, GL_FLOAT, 0, back)
    glDrawArrays(GL_POLYGON, 0, 4)
    front = [[-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5]]
    glVertexPointer(3, GL_FLOAT, 0, front)
    # glTexCoordPointer(8, GL_FLOAT, 0, front)
    glDrawArrays(GL_POLYGON, 0, 4)
    right = [[-0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5]]
    # tright = [[-0.5 + 0.27 * 2, -0.5 + 0.25 * 2], [0.5+ 0.27* 2, 0.5+ 0.25* 2] ,[0.5+ 0.27* 2, -0.5+ 0.25* 2],[-0.5+ 0.27* 2, 0.5+ 0.25* 2]]
    glVertexPointer(3, GL_FLOAT, 0, right)
    # glTexCoordPointer(3, GL_FLOAT, 0, tright)

    # glTexCoordPointer(2, GL_FLOAT, 0, right)
    glDrawArrays(GL_POLYGON, 0, 4)
    left = [[-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5]]
    glVertexPointer(3, GL_FLOAT, 0, left)
    # glTexCoordPointer(3, GL_FLOAT, 0, left)
    glDrawArrays(GL_POLYGON, 0, 4)
    top = [[0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5], [0.5, -0.5, 0.5]]
    glVertexPointer(3, GL_FLOAT, 0, top)
    # glTexCoordPointer(3, GL_FLOAT, 0, top)
    glDrawArrays(GL_POLYGON, 0, 4)
    bottom = [[-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5]]
    glVertexPointer(3, GL_FLOAT, 0, bottom)
    # glTexCoordPointer(3, GL_FLOAT, 0, bottom)
    glDrawArrays(GL_POLYGON, 0, 4)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    glDisableClientState(GL_VERTEX_ARRAY)



# def Cube(cubeverts):
#    glBegin(GL_POLYGON)
#    for surf in surfs:
#        n = 0
#        for vertex in surf:
#            if n == 0:
#                xv = 0.0
#                yv = 0.0
#            if n == 1:
#                xv = 1.0
#                yv = 0.0
#            if n == 2:
#                xv = 1.0
#                yv = 1.0
#            if n == 3:
#                xv = 0.0
#                yv = 1.0
#            glTexCoord2f(xv,yv)
#            glVertex3fv(cubeverts[vertex])
#            n += 1
#    glEnd()
#

def light_on():
    glCallList(2)


def light_display_list():
    glNewList(2, GL_COMPILE)
    material_diffuse = [1, 1.0, 1.0, 1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_diffuse)
    light3_diffuse = [1, 1, 1]
    light3_position = [0.0, 0.0, 1.0, 0.0]
    light3_spot_direction = [0.0, 0.0, -1.0]
    glEnable(GL_LIGHT0)

    glEnable(GL_LIGHTING)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glEnable(GL_NORMALIZE)

    glLightfv(GL_LIGHT0, GL_DIFFUSE, light3_diffuse)
    glLightfv(GL_LIGHT0, GL_POSITION, light3_position)
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 10)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light3_spot_direction)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, Kl)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, Kq)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, Kc)
    glEndList()


def display(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if light:
        light_on()
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    if not moving:
        glPushMatrix()
        drawFigure(0, 0, 0, x, y, z, 0.3)
        glPopMatrix()
    if moving:
        global h03
        global v0
        glPushMatrix()
        drawFigure(0, h0, 0, x, y, z, 0.3)
        h0 += v0
        v0 -= g
        if h0 <= surface or h0 > 0:
            v0 = -1 * v0
        glPopMatrix()

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global x
    global y
    global z
    global sc
    global light
    global moving
    global light_position
    global material_diffusion
    global Kl
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            sc += 0.01
        if key == glfw.KEY_DOWN:
            sc -= 0.01
        if key == 49:
            light_position[2] -= 0.65
        if key == 50:
            light_position[2] += 0.65
        if key == 51:
            x += 2.5
            y += 2.5
        if key == 52:
            x -= 2.5
            y -= 2.5
        if key == glfw.KEY_ENTER:
            if light:
                light = False
                glDisable(GL_LIGHTING)
            else:
                glEnable(GL_LIGHTING)
                glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
                glEnable(GL_NORMALIZE)
                light = True
        if key == glfw.KEY_DOWN:

            if moving:
                global h0
                global v0
                v0 = 0
                h0 = 0
                moving = False
            else:
                moving = True
        if key == glfw.KEY_UP:
            global it
            if it:
                glDisable(GL_TEXTURE_2D)
            else:
                glEnable(GL_TEXTURE_2D)
            it = not it


def main():

    if not glfw.init():
        return
    window = glfw.create_window(600, 600, "lab7", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glClearColor(0.0, 0.0, .1, 1.0)

    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_FRONT)
    # glFrontFace(GL_CW)

    glGenTextures(1, texture)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, (1, 1, 0, 1))
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


main()
