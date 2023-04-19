import math
import glfw
import random
from OpenGL.GL import *
import numpy as np
mult = lambda a, b: a.x * b.x + a.y * b.y
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
    global cx, cy, fl, futurepointsup, futurepointsdown, upright, downleft,vertices, lineseVertices,mass_center
    if action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_LEFT:
            if fl  == 0:
 
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
                    edge =([[vertices[len(vertices) - 2][0], vertices[len(vertices) - 2][1]],[vertices[len(vertices) - 1][0],
                             vertices[len(vertices) - 1][1]]])
                    edges.append(edge)
                    mass_center += cx

            else: 
                drawpixel(cx, cy)
                 
                lineseVertices.append([cx, cy])
                if len(lineseVertices) % 2 == 0:
                    drawline(lineseVertices[len(lineseVertices) - 2][0], lineseVertices[len(lineseVertices) - 2][1], lineseVertices[len(lineseVertices) - 1][0],
                             lineseVertices[len(lineseVertices) - 1][1])
def drawpixelGreen(x, y):
    index = round(x) * 2 * 3 + round(y) * 2 * 1000 * 3
     
    for i in range(index-3000, index-3000 + 6):
        buffer[i] = 0
        buffer[i+2] = 0
        buffer[i+3] = 255  
    for i in range(index, index + 6):
        buffer[i] = 0
        buffer[i+2] = 0
        buffer[i+3] = 255 
    for i in range(index + 3000, index + 3006):
        buffer[i] = 0
        buffer[i+2] = 0
        buffer[i+3] = 255
def drawpixelRed(x, y):
    index = round(x) * 2 * 3 + round(y) * 2 * 1000 * 3
 
    for i in range(index, index + 6):
        buffer[i] = 0
        buffer[i+1] = 255
 
    for i in range(index + 3000, index + 3006):
        buffer[i] = 0
        buffer[i+1] = 255

def mult(a,b):
    return a[0] * b[0] + a[1] * b[1]
def isInternal(N, i):
    edgeX = vertices[(i+2)%len(vertices)][0] - vertices[i][0]
    edgeY = vertices[(i+2)%len(vertices)][1] - vertices[i][1]
    return mult([edgeX,edgeY], N) > 0
def cyrusBeck(P1X, P1Y, P2X,  P2Y):

    #global gP2X, gP1X, gP2Y, gP1Y
    t_b = 0.0
    t_e = 1.0
    dirLX = P2X - P1X
    dirLY = P2Y - P1Y
    bP1X = P1X
    bP1Y = P1Y
    bP2X = P2X
    bP2Y = P2Y
    
    counter = 0
    for i in range(len(vertices)):
        gP1X = 0
        gP2X = 0
        gP1Y = 0
        gP2Y = 0
        edgeDirX = vertices[(i+1)%len(vertices)][0] - vertices[i][0]
        edgeDirY = vertices[(i+1)%len(vertices)][1] - vertices[i][1]
        edgeDir = [edgeDirX, edgeDirY]
        N = [-edgeDirY, edgeDirX]
        if(not isInternal(N, i)):
            N = [edgeDirY, -edgeDirX]

        counter+=1
        drawlineRed((vertices[i][0] + vertices[(i+1)%len(vertices)][0])/2 ,(vertices[i][1] + vertices[(i+1)%len(vertices)][1])/2,(vertices[i][0] + vertices[(i+1)%len(vertices)][0])/2+ N[0],(vertices[i][1] + vertices[(i+1)%len(vertices)][1])/2+ N[1])
       
        Qx = P1X - (vertices[i][0] + vertices[(i+1)%len(vertices)][0])/2
        Qy = P1Y - (vertices[i][1] + vertices[(i+1)%len(vertices)][1])/2
        dirL = [dirLX, dirLY]

        Q = [Qx, Qy]
        Pn = mult(dirL, N)

        Qn = mult(Q, N)
        if(Pn == 0):
            if(Qn < 0):
                break
            else:
                continue
 
        else:
            t = - float(Qn) / float(Pn)
      
            if Pn > 0:
                if t >= t_e:
                    continue 
                t_b = max(t_b, t)
            else:
                if t <= t_b:
                    continue
                t_e = min(t_e, t)
       
        
            gP1X = (P1X + t_b * dirLX)
            gP1Y =  (P1Y + t_b * dirLY)
           
            P2X = (P1X +t_e * dirLX)
            P2Y = (P1Y + t_e * dirLY)
            print(gP1X ,gP1Y,P2X,P2Y)
    drawlineGreen(gP1X, gP1Y, P2X, P2Y)

            

       
  


        
        
         

def perpendicular( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b
mass_center = 0
lineseVertices = []
def cyrusBecking():
    print(len(lineseVertices))
    for i in range(0, len(lineseVertices),2):
        P1X = lineseVertices[i][0]
        P1Y = lineseVertices[i][1]
        P2X = lineseVertices[(i+1)%len(lineseVertices)][0]
        P2Y = lineseVertices[(i+1)%len(lineseVertices)][1]
        cyrusBeck(P1X, P1Y, P2X, P2Y)
edges = []
def normalize(a):
    a = np.array(a)
    return a/np.linalg.norm(a) 
def key_callback(window, key, scancode, action, mods):
    global vertices, fl, cx, cy, futurepointsup, futurepointsdown, downleft, upright, lineseVertices,mass_center
    if action == glfw.PRESS:
        if key == glfw.KEY_ENTER:
            if fl == 0:
                fl = 1
                drawline(vertices[len(vertices) - 1][0], vertices[len(vertices) - 1][1], vertices[0][0], vertices[0][1])
                edges.append([[vertices[len(vertices) - 1][0],
                             vertices[len(vertices) - 1][1]],[vertices[0][0], vertices[0][1]]])
                mass_center = mass_center / (len(vertices))
        
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

        if key == glfw.KEY_BACKSPACE:
            cyrusBecking()

 
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
def drawlineRed(x1, y1, x2, y2):
   
    length = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    vector = ((x2 - x1) / length, (y2 - y1) / length)
 
    while True:
        x1 += vector[0]
        y1 += vector[1]
        drawpixelRed(x1, y1)
        if math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)) < 1:
            break
def drawlineGreen(x1, y1, x2, y2):
   
    length = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    vector = ((x2 - x1) / length, (y2 - y1) / length)
 
    while True:
        x1 += vector[0]
        y1 += vector[1]
        drawpixelGreen(x1, y1)
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
