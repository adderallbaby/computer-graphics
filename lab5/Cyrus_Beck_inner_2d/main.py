import math
import random
import glfw
from OpenGL.GL import *

"""

АЛГОРИТМ КИРУСА_БЕКА
Обрезает все снаружи, остаются только объекты внутри
2D

Еще рисует внутренние нормали к каждой из сторон окна (и пруф что они нормали)
"""

buffer = bytearray(1000 * 1000 * 3)
cx = 0
cy = 0
vertices = []
toClean = bytearray(1000 * 1000 * 3)
fl = 0
minX = 1000000
maxX = -1
maxY = -1
minY = 100000
lineseVertices = []

for j in range(0, 1000 * 1000):
    toClean[j * 3 + 1] = 0
    toClean[j * 3 + 2] = 0
    toClean[j * 3] = 0
    buffer[j * 3] = 0
    buffer[j * 3 + 1] = 0
    buffer[j * 3 + 2] = 0


def cursor_pos(window, xpos, ypos):
    global cx, cy
    cx = round(xpos)
    cy = round(500 - ypos)


def mouse_button(window, button, action, mods):
    global cx, cy, fl, vertices, lineseVertices, mass_center
    if action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_LEFT:
            if fl == 0:
                drawpixelCustom(cx, cy, [255, 255, 255])
                vertices.append([cx, cy])
                if len(vertices) > 1:
                    drawlineCustom(
                        vertices[len(vertices) - 2][0],
                        vertices[len(vertices) - 2][1],
                        vertices[len(vertices) - 1][0],
                        vertices[len(vertices) - 1][1],
                        [255, 255, 255],
                    )
            else:
                drawpixelCustom(cx, cy, [255, 255, 255])

                lineseVertices.append([cx, cy])
                if len(lineseVertices) % 2 == 0:
                    drawlineCustom(
                        lineseVertices[len(lineseVertices) - 2][0],
                        lineseVertices[len(lineseVertices) - 2][1],
                        lineseVertices[len(lineseVertices) - 1][0],
                        lineseVertices[len(lineseVertices) - 1][1],
                        [255, 255, 255],
                    )


def drawpixelCustom(x, y, color):
    index = round(x) * 2 * 3 + round(y) * 2 * 1000 * 3
    for i in range(index - 3000, index - 3000 + 6, 3):
        buffer[i] = color[0]
        buffer[i + 1] = color[1]
        buffer[i + 2] = color[2]
    for i in range(index, index + 6, 3):
        buffer[i] = color[0]
        buffer[i + 1] = color[1]
        buffer[i + 2] = color[2]
    for i in range(index + 3000, index + 3000 + 6, 3):
        buffer[i] = color[0]
        buffer[i + 1] = color[1]
        buffer[i + 2] = color[2]


def inside(x, y):
    return x < maxX and x > minX and y < maxY and y > minY


def mult(a, b):
    return a[0] * b[0] + a[1] * b[1]


def isInternal(N, i):
    edgeX = vertices[(i + 2) % len(vertices)][0] - vertices[i][0]
    edgeY = vertices[(i + 2) % len(vertices)][1] - vertices[i][1]
    return mult([edgeX, edgeY], N) > 0


def cyrusBeck(P1X, P1Y, P2X, P2Y):
    global minX

    t_b = 0.0
    t_e = 1.0
    dirLX = P2X - P1X
    dirLY = P2Y - P1Y
    bP1X = P1X
    bP1Y = P1Y

    counter = 0
    do = False
    for i in range(len(vertices)):
        edgeDirX = vertices[(i + 1) % len(vertices)][0] - vertices[i][0]
        edgeDirY = vertices[(i + 1) % len(vertices)][1] - vertices[i][1]

        N = [-edgeDirY, edgeDirX]
        if not isInternal(N, i):
            N = [edgeDirY, -edgeDirX]

        counter += 1
        drawlineCustom(
            (vertices[i][0] + vertices[(i + 1) % len(vertices)][0]) / 2,
            (vertices[i][1] + vertices[(i + 1) % len(vertices)][1]) / 2,
            (vertices[i][0] + vertices[(i + 1) % len(vertices)][0]) / 2 + N[0] / 5,
            (vertices[i][1] + vertices[(i + 1) % len(vertices)][1]) / 2 + N[1] / 5,
            [255, 0, 0],
        )
        drawRectangle(
            (vertices[i][0] + vertices[(i + 1) % len(vertices)][0]) / 2 + N[0] / 15,
            (vertices[i][1] + vertices[(i + 1) % len(vertices)][1]) / 2 + N[1] / 15,
            [-N[1], N[0]],
            [255, 0, 0],
        )
        Qx = P1X - (vertices[i][0] + vertices[(i + 1) % len(vertices)][0]) / 2
        Qy = P1Y - (vertices[i][1] + vertices[(i + 1) % len(vertices)][1]) / 2
        dirL = [dirLX, dirLY]

        Q = [Qx, Qy]
        Pn = mult(dirL, N)
        Qn = mult(Q, N)

        if not doIntersect(
            P1X,
            P1Y,
            P2X,
            P2Y,
            vertices[i][0],
            vertices[i][1],
            vertices[(i + 1) % len(vertices)][0],
            vertices[(i + 1) % len(vertices)][1],
        ) and not inside((P1X + P2X) / 2, (P1Y + P2Y) / 2):
            continue
        else:
            do = True
            t = -float(Qn) / float(Pn)

            if Pn > 0:
                if t >= t_e:
                    continue
                t_b = max(t_b, t)
            else:
                if t <= t_b:
                    continue
                t_e = min(t_e, t)

            bP1X = P1X + t_b * dirLX
            bP1Y = P1Y + t_b * dirLY

            P2X = P1X + t_e * dirLX
            P2Y = P1Y + t_e * dirLY

    if do == True:
        drawlineCustom(bP1X, bP1Y, P2X, P2Y, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        # drawlineCustom(P1X, P1Y, bP1X, bP1Y,[random.randint(0,255),random.randint(0,255),random.randint(0,255)])
        # drawlineCustom(P2X, P2Y, bP2X, bP2Y,[random.randint(0,255),random.randint(0,255),random.randint(0,255)])


def doIntersect(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    v1 = (bx2 - bx1) * (ay1 - by1) - (by2 - by1) * (ax1 - bx1)
    v2 = (bx2 - bx1) * (ay2 - by1) - (by2 - by1) * (ax2 - bx1)
    v3 = (ax2 - ax1) * (by1 - ay1) - (ay2 - ay1) * (bx1 - ax1)
    v4 = (ax2 - ax1) * (by2 - ay1) - (ay2 - ay1) * (bx2 - ax1)
    return (v1 * v2) < 0 and (v3 * v4) < 0


def drawRectangle(x, y, vector, color):
    drawlineCustom(x, y, x + vector[0] / 15, y + vector[1] / 15, color)
    drawlineCustom(
        x + vector[0] / 15,
        y + vector[1] / 15,
        x + vector[0] / 15 + (-vector[1]) / 15,
        y + vector[1] / 15 + vector[0] / 15,
        color,
    )


def cyrusBecking():
    for i in range(0, len(lineseVertices), 2):
        P1X = lineseVertices[i][0]
        P1Y = lineseVertices[i][1]
        P2X = lineseVertices[(i + 1) % len(lineseVertices)][0]
        P2Y = lineseVertices[(i + 1) % len(lineseVertices)][1]
        drawlineCustom(P1X, P1Y, P2X, P2Y, [0, 0, 0])
        cyrusBeck(P1X, P1Y, P2X, P2Y)


def drawlineCustom(x1, y1, x2, y2, color):
    length = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    vector = ((x2 - x1) / length, (y2 - y1) / length)
    drawpixelCustom(x1, y1, color)

    while True:
        x1 += vector[0]
        y1 += vector[1]
        drawpixelCustom(x1, y1, color)
        if math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)) < 1:
            break


def key_callback(window, key, scancode, action, mods):
    global vertices, fl, cx, cy, upright, lineseVertices, mass_center, minX, minY, maxX, maxY, toClean, buffer
    if action == glfw.PRESS:
        if key == glfw.KEY_ENTER:
            if fl == 0:
                fl = 1
                drawlineCustom(
                    vertices[len(vertices) - 1][0],
                    vertices[len(vertices) - 1][1],
                    vertices[0][0],
                    vertices[0][1],
                    [255, 255, 255],
                )

                for i in range(len(vertices)):
                    x = (vertices[i][0] + vertices[(i + 1) % len(vertices)][0]) / 2
                    y = (vertices[i][1] + vertices[(i + 1) % len(vertices)][1]) / 2
                    if x < minX:
                        minX = x
                    if x > maxX:
                        maxX = x
                    if y < minY:
                        minY = y
                    if y > maxY:
                        maxY = y

        if key == glfw.KEY_BACKSPACE:
            if len(lineseVertices) % 2 == 0:
                cyrusBecking()
        if key == glfw.KEY_C:
            buffer = toClean.copy()
            vertices = []
            lineseVertices = []
            fl = 0
            cx = 0
            cy = 0


def main():
    if not glfw.init():
        return

    window = glfw.create_window(500, 500, "lab5", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, cursor_pos)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_key_callback(window, key_callback)
    glClearColor(0, 0, 1, 1)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDrawPixels(1000, 1000, GL_RGB, GL_UNSIGNED_BYTE, buffer)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


main()
