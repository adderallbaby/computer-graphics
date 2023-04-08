import math
import glfw
from OpenGL.GL import *
 
buffer = bytearray(1000 * 1000 * 3)
cx = 0
cy = 0
vertices = []
futurepointsup = []
futurepointsdown = []
fl = 0
 
for j in range(0, 1000 * 1000):
    buffer[j * 3] = 0
    buffer[j * 3 + 1] = 0
    buffer[j * 3 + 2] = 0
 
 
def cursor_pos(window, xpos, ypos):
    global cx, cy
    cx = round(xpos)
    cy = round(500 - ypos)
 
 
def mouse_button(window, button, action, mods):
    global cx, cy, fl, futurepointsup, futurepointsdown
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
 
                filllinedown(cx, cy-1)
                   
                counter = 0
                while True:
                    if counter >= len(futurepointsdown):
                        break
                    filllinedown(futurepointsdown[counter][0], futurepointsdown[counter][1])
                    counter += 1
                fl = 2
                slidingWindow()
                glDrawPixels(1000,1000,GL_RGB,GL_UNSIGNED_BYTE,buffer)
                return
            drawpixel(cx, cy)
            vertices.append([cx, cy])
            if len(vertices) > 1:
                drawline(vertices[len(vertices) - 2][0], vertices[len(vertices) - 2][1], vertices[len(vertices) - 1][0],
                         vertices[len(vertices) - 1][1])
            
 
def key_callback(window, key, scancode, action, mods):
    global vertices, fl
    if action == glfw.PRESS:
        if key == glfw.KEY_ENTER:
            if fl == 0:
                fl = 1
                drawline(vertices[len(vertices) - 1][0], vertices[len(vertices) - 1][1], vertices[0][0], vertices[0][1])
 
 
def drawpixel(x, y):
    index = round(x) * 2 * 3 + round(y) * 2 * 1000 * 3
    buffer[index] =255 
    buffer[index + 1] = 255
    buffer[index + 2] = 100

 
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
 
 
'''
def fillline(x, y):
    while True:
        if not check(x, y):
            drawpixel(x, y)
        else:
            return
        fillline(x + 1, y)
        fillline(x - 1, y)
'''
 
 
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
def getAllPixels(i):
     toUpdateR =0
     counter = 0
     toUpdateR += buffer[i-3]
     toUpdateR += buffer[i+3]
     toUpdateR += buffer[i+3000]
     toUpdateR += buffer[i+3003]
     toUpdateR += buffer[i+2997]
     toUpdateR += (buffer[i-3003])
     toUpdateR += (buffer[i-2997])
     toUpdateR += buffer[i-3000]

     return toUpdateR // 9
def updateAllNeighbours(i ,newVal):
    buffer[i] = newVal #+ 15
    buffer[i-3] = newVal# + 15
    buffer[i+3] =newVal #+ 15
    buffer[i+3000] = newVal# + 15
    buffer[i+3003] = newVal #+ 15
    buffer[i+2997] = newVal #+ 15
    buffer[i-3003] = newVal #+ 15
    buffer[i-3000] = newVal #+ 15
    buffer[i-2997] = newVal #+ 15
def slidingWindow():
    for i in range(3003, len(buffer) - 3003):
        if(buffer[i] != 0 or buffer[i+1] != 0 or buffer[i+2] !=0):
            
            toUpdateR = getAllPixels(i) 
            toUpdateG = getAllPixels(i+1) 
            toUpdateB = getAllPixels(i+2) 
            updateAllNeighbours(i, toUpdateR)
            updateAllNeighbours(i+1, toUpdateG)
            updateAllNeighbours(i+2, toUpdateB)


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
