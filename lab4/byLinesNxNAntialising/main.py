import math
import glfw
import random
from OpenGL.GL import *
 
buffer = bytearray(1000 * 1000 * 3)
cx = 0
cy = 0
vertices = []
futurepointsup = []
futurepointsdown = []
fl = 0
downleft = [500, 500]
upright = [0, 0]
 
for j in range(0, 1000 * 1000):
    buffer[j * 3] = 0
    buffer[j * 3 + 1] = 0
    buffer[j * 3 + 2] = 0
 
 
def cursor_pos(window, xpos, ypos):
    global cx, cy
    cx = round(xpos)
    cy = round(500 - ypos)
 
 
def mouse_button(window, button, action, mods):
    global cx, cy, fl, futurepointsup, futurepointsdown, upright, downleft
    if fl == 2:
        return
    if action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_LEFT:
            if fl == 1:
 
                filllineup(cx, cy)
 
                counter = 0
                while True:
                    if counter >= len(futurepointsup):
                        break
                    filllineup(futurepointsup[counter][0], futurepointsup[counter][1])
                    counter += 1
 
                filllinedown(cx, cy - 1)
 
                counter = 0
                while True:
                    if counter >= len(futurepointsdown):
                        break
                    filllinedown(futurepointsdown[counter][0], futurepointsdown[counter][1])
                    counter += 1
                fl = 2
                slidingWindow()
                return
 
            if cx > upright[0]:
                upright[0] = cx
 
            if cx < downleft[0]:
                downleft[0] = cx
 
            if cy > upright[1]:
                upright[1] = cy
 
            if cy < downleft[1]:
                downleft[1] = cy
 
            drawpixel(cx, cy)
            vertices.append([cx, cy])
            if len(vertices) > 1:
                drawline(vertices[len(vertices) - 2][0], vertices[len(vertices) - 2][1], vertices[len(vertices) - 1][0],
                         vertices[len(vertices) - 1][1])
 
 
def key_callback(window, key, scancode, action, mods):
    global vertices, fl, cx, cy, futurepointsup, futurepointsdown, downleft, upright
    if action == glfw.PRESS:
        if key == glfw.KEY_ENTER:
            if fl == 0:
                fl = 1
                drawline(vertices[len(vertices) - 1][0], vertices[len(vertices) - 1][1], vertices[0][0], vertices[0][1])
            else:
                cx = 0
                cy = 0
                vertices = []
                futurepointsup = []
                futurepointsdown = []
                fl = 0
                downleft = [500, 500]
                upright = [0, 0]
 
                for i in range(0, 1000 * 1000):
                    buffer[i * 3] = 0
                    buffer[i * 3 + 1] = 0
                    buffer[i * 3 + 2] = 0
 
 
def drawpixel(x, y):
    index = round(x) * 2 * 3 + round(y) * 2 * 1000 * 3
 
    for i in range(index, index + 6):
        buffer[i] = 255
 
    for i in range(index + 3000, index + 3006):
        buffer[i] = 255
 
 
def drawline(x1, y1, x2, y2):
    length = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    vector = ((x2 - x1) / length, (y2 - y1) / length)
 
    while True:
        x1 += vector[0]
        y1 += vector[1]
        drawpixel(x1, y1)
        if math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)) < 1:
            break
 
 
def check(x, y):
    index = round(x) * 2 * 3 + round(y) * 2 * 1000 * 3
    if index >= len(buffer):
        return True
    if buffer[index] != 0 or buffer[index + 1] != 0 or buffer[index + 2] != 0:
        return True
    else:
        return False
 
 
def filllineup(x, y):
    if check(x, y):
        return
 
    global futurepointsup
    up = False
    x0 = x
 
    while True:
 
        if check(x, y):
            minx = x + 1
            break
 
        if not up and not check(x, y + 1):
            futurepointsup.append([x, y + 1])
            up = True
 
        if check(x, y + 1):
            up = False
 
        x -= 1
 
    x = x0
    while True:
 
        if check(x, y):
            maxx = x
            break
 
        if not up and not check(x, y + 1):
            futurepointsup.append([x, y + 1])
            up = True
 
        if check(x, y + 1):
            up = False
 
        x += 1
 
    for i in range(minx, maxx):
        drawpixel(i, y)
 
 
def filllinedown(x, y):
    if check(x, y):
        return
 
    global futurepointsdown
    down = False
    x0 = x
 
    while True:
 
        if check(x, y):
            minx = x + 1
            break
 
        if not down and not check(x, y - 1):
            futurepointsdown.append([x, y - 1])
            down = True
 
        if check(x, y + 1):
            down = False
 
        x -= 1
 
    x = x0
    while True:
 
        if check(x, y):
            maxx = x
            break
 
        if not down and not check(x, y - 1):
            futurepointsdown.append([x, y - 1])
            down = True
 
        if check(x, y - 1):
            down = False
 
        x += 1
 
    for i in range(minx, maxx):
        drawpixel(i, y)
 
 
def getAllPixels(i):
    toUpdateR = 0
    toUpdateR += buffer[i + 3]
    toUpdateR += buffer[i - 3]
    toUpdateR += buffer[i + 3000]
    toUpdateR += buffer[i - 3000]
    toUpdateR += buffer[i + 3003]
    toUpdateR += (buffer[i - 3003])
    toUpdateR += buffer[i + 2997]
    toUpdateR += (buffer[i - 2997])
 
    return toUpdateR // 8
 
 
def updateAllNeighbours(i, newVal):
    buffer[i] = newVal
    buffer[i - 3] = newVal
    buffer[i + 3] = newVal
    buffer[i + 3000] = newVal
    buffer[i + 3003] = newVal
    buffer[i + 2997] = newVal
    buffer[i - 3003] = newVal
    buffer[i - 3000] = newVal
    buffer[i - 2997] = newVal
 
 
def slidingWindow():
    start = downleft[0] * 2 * 3 + downleft[1] * 2 * 1000 * 3
    end = upright[0] * 2 * 3 + upright[1] * 2 * 1000 * 3
    for i in range(start, end):
        if buffer[i] != 0 or buffer[i + 1] != 0 or buffer[i + 2] != 0:
            toUpdateR = getAllPixels(i)
            toUpdateG = getAllPixels(i + 1)
            toUpdateB = getAllPixels(i + 2)
            updateAllNeighbours(i, toUpdateR)
            updateAllNeighbours(i + 1, toUpdateG)
            updateAllNeighbours(i + 2, toUpdateB)
 
 
def main():
    if not glfw.init():
        return
 
    window = glfw.create_window(500, 500, "lab4", None, None)
 
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
