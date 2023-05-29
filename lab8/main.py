import glfw
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image as Image
import numpy
 
x = 0
y = 0
vx = 0.04
vy = 0.02
moving = False
 
rot = 0
rot2 = 0
scale = 0.5
is_texturing_enabled = True
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
            if len(rows) !=512:
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
 
def program():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "lab8", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    setup()
 
    while not glfw.window_should_close(window):
        prepare()
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()
 
    glfw.destroy_window(window)
    glfw.terminate()
 
 
def key_callback(window, key, scancode, action, mods):
    global rot, rot2, is_texturing_enabled, moving
 
    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            rot -= 3
        if key == glfw.KEY_LEFT:
            rot += 3
        if key == glfw.KEY_UP:
            rot2 += 3
        if key == glfw.KEY_DOWN:
            rot2 -= 3
        if key == glfw.KEY_C:
            is_texturing_enabled = not is_texturing_enabled
            print("hello")
        if key == glfw.KEY_ENTER:
            moving = not moving
 
 
def setup():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-0.1, 0.1, -0.1, 0.1, 0.2, 1000)
 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
 
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 0.5])
 
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
 
    load_texture()
 
    # Положение вершин не меняется
    # Цвет вершины - такой же как и в массиве цветов
    vertex = create_shader(GL_VERTEX_SHADER, """
    varying vec3 n;
    varying vec3 v;
    varying vec2 uv;
    void main()
    {   
        uv = gl_MultiTexCoord0.xy;
        v = vec3(gl_ModelViewMatrix * gl_Vertex);
        n = normalize(gl_NormalMatrix * gl_Normal);
        gl_TexCoord[0] = gl_TextureMatrix[0]  * gl_MultiTexCoord0;
        gl_Position = ftransform();
    }
 
 
    """)
 
    # Определяет цвет каждого фрагмента как "смешанный" цвет его вершин
    fragment = create_shader(GL_FRAGMENT_SHADER, """
    varying vec3 n;
    varying vec3 v; 
    uniform sampler2D tex;
    void main ()  
    {  
        vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
        vec3 E = normalize(-v);
        vec3 R = normalize(-reflect(L,n));  
 
        //calculate Ambient Term:  
        vec4 Iamb = gl_FrontLightProduct[0].ambient;    
 
        //calculate Diffuse Term:  
        vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(n,L), 0.0);
        Idiff = clamp(Idiff, 0.0, 1.0);     
 
        // calculate Specular Term:
        vec4 Ispec = gl_LightSource[0].specular 
                        * pow(max(dot(R,E),0.0),0.3);
        Ispec = clamp(Ispec, 0.0, 1.0); 
 
        vec4 texColor = texture2D(tex, gl_TexCoord[0].st);
        gl_FragColor = (Idiff + Iamb + Ispec) * texColor;
    }
    """)
 
    program = glCreateProgram()
 
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
 
    glLinkProgram(program)
 
    glUseProgram(program)
 
texture = 0
def load_texture():
    rows = read_rows("7.bmp")
    image = repack_sub_pixels(rows)   
    glGenTextures(1, texture)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D) 
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, (1,1,0,1))
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
 
 
def prepare():
    glClearColor(0.5, 0.5, 0.5, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
 
def display():
    global rot, scale, moving, x, y, vx, vy, is_texturing_enabled
    glPushMatrix()
    glRotatef(-60, 1, 0, 0)
    glRotatef(33, 0, 0, 1)
    glTranslatef(2, 3, -2.5)
 
    glRotatef(rot, 0, 0, 1)
    glRotatef(rot2, 1, 1, 1)
    glScalef(scale, scale, scale)
 
    glPushMatrix()
 
    if moving:
        glTranslatef(x, y, 0)
        x += vx
        y += vy
 
        if x >= 3 and vx > 0:
            vx *= -1
        if x <= -3 and vx < 0:
            vx *= -1
 
        if y >= 3 and vy > 0:
            vy *= -1
        if y <= -3 and vy < 0:
            vy *= -1
    else:
        glTranslatef(0, 0, 0)
        x = 0
        y = 0

    glEnable(GL_DEPTH_TEST)

    lines = False


    glRotatef(1, 1, 0, 0)
    glRotatef(2, 0, 1, 0)
    glRotatef(3, 0, 0, 1)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    back = [[-0.5  , 0.5 , -0.5 ], [-0.5 , -0.5 , -0.5 ], [0.5 , -0.5 , -0.5 ], [0.5 , 0.5 , -0.5 ]]
    tback = [[-0.5 + 0.27 * 2, -0.5 + 0.25 * 2], [-0.5+ 0.27* 2, 0.5+ 0.25* 2],[0.5+ 0.27* 2, 0.5+ 0.25* 2] ,[0.5+ 0.27* 2, -0.5+ 0.25* 2]   ]

    glEnableClientState(GL_VERTEX_ARRAY)
    glTexCoordPointer(2, GL_FLOAT, 0, tback)

    glVertexPointer(3, GL_FLOAT, 0, back)
    glDrawArrays(GL_POLYGON, 0, 4)
    front = [[-0.5 , 0.5 , 0.5 ], [-0.5 , -0.5 , 0.5 ], [0.5 , -0.5 , 0.5 ], [0.5 , 0.5 , 0.5 ]]
    glVertexPointer(3, GL_FLOAT, 0, front)
    #glTexCoordPointer(8, GL_FLOAT, 0, front)
    glDrawArrays(GL_POLYGON, 0, 4)
    right = [[-0.5 , 0.5 , 0.5 ],  [0.5 , 0.5 , 0.5 ], [0.5 , 0.5 , -0.5 ],[-0.5 , 0.5 , -0.5 ]]
    #tright = [[-0.5 + 0.27 * 2, -0.5 + 0.25 * 2], [0.5+ 0.27* 2, 0.5+ 0.25* 2] ,[0.5+ 0.27* 2, -0.5+ 0.25* 2],[-0.5+ 0.27* 2, 0.5+ 0.25* 2]]
    glVertexPointer(3, GL_FLOAT, 0, right)
    #glTexCoordPointer(3, GL_FLOAT, 0, tright)



    #glTexCoordPointer(2, GL_FLOAT, 0, right)
    glDrawArrays(GL_POLYGON, 0, 4)
    left = [[-0.5 , -0.5 , 0.5 ],  [0.5 , -0.5 , 0.5 ], [0.5 , -0.5 , -0.5 ],[-0.5 , -0.5 , -0.5 ]]
    glVertexPointer(3, GL_FLOAT, 0, left)
    #glTexCoordPointer(3, GL_FLOAT, 0, left)
    glDrawArrays(GL_POLYGON, 0, 4)
    top = [[0.5 , -0.5 , -0.5 ], [0.5 , 0.5 , -0.5 ], [0.5 , 0.5 , 0.5 ], [0.5 , -0.5 , 0.5 ]]
    glVertexPointer(3, GL_FLOAT, 0, top)
    #glTexCoordPointer(3, GL_FLOAT, 0, top)
    glDrawArrays(GL_POLYGON, 0, 4)
    bottom =  [[-0.5 , -0.5 , -0.5 ], [-0.5 , 0.5 , -0.5 ], [-0.5 , 0.5 , 0.5 ], [-0.5 , -0.5 , 0.5 ]]
    glVertexPointer(3, GL_FLOAT, 0, bottom)
   # glTexCoordPointer(3, GL_FLOAT, 0, bottom)
    glDrawArrays(GL_POLYGON, 0, 4)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)


    glDisableClientState(GL_VERTEX_ARRAY)






    glutSwapBuffers()

 

 
    glPopMatrix()
 
    glPushMatrix()
    glRotatef(45, 0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 1, 0))
 
    glScalef(0.2, 0.2, 0.2)
    glColor3f(1, 1, 1)
    glPopMatrix()
 
    glPopMatrix()
    glutSwapBuffers()
 
    glutPostRedisplay()
 
 
# Процедура подготовки шейдера (тип шейдера, текст шейдера)
def create_shader(shader_type, source):
    # Создаем пустой объект шейдера
    shader = glCreateShader(shader_type)
    # Привязываем текст шейдера к пустому объекту шейдера
    glShaderSource(shader, source)
    # Компилируем шейдер
    glCompileShader(shader)
    # Возвращаем созданный шейдер
    return shader
 
 
program()
