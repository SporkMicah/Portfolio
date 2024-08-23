import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random

#define the faces
faces = [
    [0, 8, 10, 2, 12],
    [1, 9, 11, 3, 13],
    [4, 8, 14, 6, 10],
    [5, 9, 15, 7, 11],
    [0, 16, 18, 4, 8],
    [1, 17, 19, 5, 9],
    [2, 10, 6, 18, 0],
    [3, 11, 7, 19, 1],
    [12, 2, 17, 13, 3],
    [14, 6, 18, 16, 0],
    [15, 7, 19, 17, 1],
    [16, 8, 12, 3, 13]
]

#define the vertices of a dodecahedron
vertices = [
    [1, 1, 1],
    [1, 1, -1],
    [1, -1, 1],
    [1, -1, -1],
    [-1, 1, 1],
    [-1, 1, -1],
    [-1, -1, 1],
    [-1, -1, -1],
    [0, 0.618, 1.618],
    [0, 0.618, -1.618],
    [0, -0.618, 1.618],
    [0, -0.618, -1.618],
    [1.618, 0, 0.618],
    [1.618, 0, -0.618],
    [-1.618, 0, 0.618],
    [-1.618, 0, -0.618],
    [0.618, 1.618, 0],
    [0.618, -1.618, 0],
    [-0.618, 1.618, 0],
    [-0.618, -1.618, 0]
]

#define the edges that connect those vertices
edges = [
    (0, 8), (0, 16), (0, 12),
    (1, 9), (1, 13), (1, 16),
    (2, 10), (2, 17), (2, 12),
    (3, 11), (3, 17), (3, 13),
    (4, 14), (4, 18), (4, 8),
    (5, 15), (5, 19), (5, 9),
    (6, 14), (6, 18), (6, 10),
    (7, 15), (7, 19), (7, 11),
    (8, 10), (9, 11), (12, 13),
    (14, 15), (16, 18), (17, 19)
]

def draw_dodecahedron():
    for face in faces:
        # Generate a random color for each face
        glColor3f(random.random(), random.random(), random.random())
        glBegin(GL_POLYGON)
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()
    
    glColor3f(1, 1, 1)  # Set color to white for the edges
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()

    # Set OpenGL attributes for multisampling (anti-aliasing)
    pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 4)  # 4x anti-aliasing

    display = (1640, 1000)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)  # Enable depth testing for correct rendering

    # Enable multisampling in OpenGL
    glEnable(GL_MULTISAMPLE)
    
    glTranslatef(0.0, 0.0, -10)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        # Rotate the dodecahedron
        glRotatef(1, 3, 1, 1)   # Main rotation (3D)
        glRotatef(0.5, 0, 1, 0) # Equatorial (around y-axis)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_dodecahedron()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()