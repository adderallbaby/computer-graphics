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
        if pixel_index == 96:
            pixel_index = 0
            rows.insert(0, row)
            if len(row) != 96 * 3:
                raise Exception("Row length is not 1920*3 but " + str(len(row)) + " / 3.0 = " + str(len(row) / 3.0))
            row = []
        pixel_index += 1

        r_string = image_file.read(1)
        g_string = image_file.read(1)
        b_string = image_file.read(1)

        if len(r_string) == 0:
            # This is expected to happen when we've read everything.
            if len(rows) != 96:
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

    diff = len(sub_pixels) - 96 * 96 * 3
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
rows = read_rows("Resize_water.bmp")
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
light_position = [0.0, 0.0, 20.0, 1.0]
material_diffusion = [1, 1, 1, 1.0]
light_diffusion = [1, 1, 1]
Kl = 0.001
Kq = 0.002
Kc = 0.001

def drawFigure(x, y, z, angle1, angle2, angle3, s):
    glScalef(s, s, s)
    glTranslatef(x, y, z)
    glRotatef(angle1, 1, 0, 0)
    glRotatef(angle2, 0, 1, 0)
    glRotatef(angle3, 0, 0, 1)
    glutSolidCube(1)


def light_on():
    global light_position
    global material_diffusion
    global light_diffusion

    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_diffusion)

    light_spot_direction = [0.0, 0.0, -1.0]
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glEnable(GL_NORMALIZE)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffusion)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 10)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_spot_direction)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, Kl)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, Kq)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, Kc)


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
        global h0
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
    if action == glfw.PRESS:
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
    window = glfw.create_window(900, 900, "lab6", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glGenTextures(1, texture)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1920, 1080, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


main()
