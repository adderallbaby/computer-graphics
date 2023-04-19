import math
import glfw
import random
from OpenGL.GL import *
import random
import math
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


            else: 
                drawpixel(cx, cy)
                 
                lineseVertices.append([cx, cy])
                if len(lineseVertices) % 2 == 0:
                    drawline(lineseVertices[len(lineseVertices) - 2][0], lineseVertices[len(lineseVertices) - 2][1], lineseVertices[len(lineseVertices) - 1][0],
                             lineseVertices[len(lineseVertices) - 1][1])
def drawpixelCustom(x, y,color):
    index = round(x) * 2 * 3 + round(y) * 2 * 1000 * 3
     
    for i in range(index-3000, index-3000 + 6,3):
        buffer[i] = color[0]
        buffer[i+1] = color[1]
        buffer[i+2] = color[2]
    for i in range(index, index + 6,3):
        buffer[i] = color[0]
        buffer[i+1] = color[1]
        buffer[i+2] = color[2]
    for i in range(index+3000, index+3000 + 6,3):
        buffer[i] = color[0]
        buffer[i+1] = color[1]
        buffer[i+2] = color[2]

def drawpixelRed(x, y):
    index = round(x) * 2 * 3 + round(y) * 2 * 1000 * 3
 
    for i in range(index, index + 6,3):
        buffer[i] = 255
        
def inside(x,y):
    print(maxX, minX,maxY,minY)
    return x < maxX and x > minX and y < maxY and y > minY
def mult(a,b):
    return a[0] * b[0] + a[1] * b[1]
def isInternal(N, i):
    edgeX = vertices[(i+2)%len(vertices)][0] - vertices[i][0]
    edgeY = vertices[(i+2)%len(vertices)][1] - vertices[i][1]
    return mult([edgeX,edgeY], N) > 0
def cyrusBeck(P1X, P1Y, P2X,  P2Y):
    global minX
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
    do = False
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
        drawLineCustom((vertices[i][0] + vertices[(i+1)%len(vertices)][0])/2 ,(vertices[i][1] + vertices[(i+1)%len(vertices)][1])/2,(vertices[i][0] + vertices[(i+1)%len(vertices)][0])/2+ N[0]/5,(vertices[i][1] + vertices[(i+1)%len(vertices)][1])/2+ N[1]/5,[255,0,0])
       
        Qx = P1X - (vertices[i][0] + vertices[(i+1)%len(vertices)][0])/2
        Qy = P1Y - (vertices[i][1] + vertices[(i+1)%len(vertices)][1])/2
        dirL = [dirLX, dirLY]

        Q = [Qx, Qy]
        Pn = mult(dirL, N)
        Qn = mult(Q, N)
        print(Pn,"Pn",  Qn, "Qn")
        if(not doIntersect(P1X,P1Y,P2X,P2Y,vertices[i][0],vertices[i][1],vertices[(i+1)%len(vertices)][0],vertices[(i+1)%len(vertices)][1]) and not inside((P1X + P2X)/2 , (P1Y + P2Y)/2)):
            print("dont")
            continue
        else:
            do = True
            t = - float(Qn) / float(Pn)
      
            if Pn > 0:
                if t >= t_e:
                    continue 
                t_b = max(t_b, t)
            else:
                if t <= t_b:
                    continue
                t_e = min(t_e, t)
       
        
            bP1X = (P1X + t_b * dirLX)
            bP1Y =  (P1Y + t_b * dirLY)
           
            P2X = (P1X +t_e * dirLX)
            P2Y = (P1Y + t_e * dirLY)
            print(gP1X ,gP1Y,P2X,P2Y)
    if(do == True):
        print(bP1X ,bP1Y,P2X,P2Y)

        drawLineCustom(bP1X, bP1Y, P2X, P2Y,[random.randint(0,255),random.randint(0,255),random.randint(0,255)])

    
minX = 1000000
maxX = -1
maxY = -1
minY = 100000
def doIntersect(ax1,ay1,ax2,ay2,bx1,by1,bx2,by2):
    v1 = (bx2-bx1)*(ay1-by1)-(by2-by1)*(ax1-bx1)
    v2 = (bx2-bx1)*(ay2-by1)-(by2-by1)*(ax2-bx1)
    v3 = (ax2-ax1)*(by1-ay1)-(ay2-ay1)*(bx1-ax1)
    v4 = (ax2-ax1)*(by2-ay1)-(ay2-ay1)*(bx2-ax1)
    return (v1*v2) < 0 and (v3*v4) < 0

        
        
         


minX= 1000000
minY = 1000000
maxX = -1

for vertice in vertices:
    if(vertice[0] < minX):
        minX = vertice[0]
lineseVertices = []
def cyrusBecking():
    print(len(lineseVertices))
    for i in range(0, len(lineseVertices),2):
        
        P1X = lineseVertices[i][0]
        P1Y = lineseVertices[i][1]
        P2X = lineseVertices[(i+1)%len(lineseVertices)][0]
        P2Y = lineseVertices[(i+1)%len(lineseVertices)][1]
        drawLineCustom(P1X,P1Y,P2X,P2Y,[0,0,0])
        cyrusBeck(P1X, P1Y, P2X, P2Y)
edges = []
def drawLineCustom(x1,y1,x2,y2,color):
       
    length = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    vector = ((x2 - x1) / length, (y2 - y1) / length)
 
    while True:
        x1 += vector[0]
        y1 += vector[1]
        drawpixelCustom(x1, y1,color)
        if math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)) < 1:
            break


def deleteLine(x,y):
    
    index = round(x) * 2 * 3 + round(y) * 2 * 1000 * 3
 
    for i in range(index, index + 6):
        buffer[i] = 0
        buffer[i+1] = 0
        buffer[i+2] = 0
    for i in range(index+3000, index+3000 + 6):
        buffer[i] = 0
        buffer[i+1] = 0
        buffer[i+2] = 0
    for i in range(index-3000, index-3000 + 6):
        buffer[i] = 0
        buffer[i+1] = 0
        buffer[i+2] = 0

def key_callback(window, key, scancode, action, mods):
    global vertices, fl, cx, cy, futurepointsup, futurepointsdown, downleft, upright, lineseVertices,mass_center,minX,minY,maxX,maxY
    if action == glfw.PRESS:
        if key == glfw.KEY_ENTER:
            if fl == 0:
                fl = 1
                drawline(vertices[len(vertices) - 1][0], vertices[len(vertices) - 1][1], vertices[0][0], vertices[0][1])
                edges.append([[vertices[len(vertices) - 1][0],
                             vertices[len(vertices) - 1][1]],[vertices[0][0], vertices[0][1]]])
                for i in range(len(vertices)):
                    x = (vertices[i][0] + vertices[(i+1)%len(vertices)][0])/2
                    y = (vertices[i][1] + vertices[(i+1)%len(vertices)][1])/2
                    if(x < minX):
                        minX = x
                    if(x > maxX):
                        maxX = x
                    if(y < minY):
                        minY = y
                    if(y > maxY):
                        maxY = y

                      
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
