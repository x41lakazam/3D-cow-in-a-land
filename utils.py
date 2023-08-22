from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class GL_BEGIN:
    def __init__(self, _type):
        self._type = _type

    def __enter__(self):
        glBegin(self._type)

    def __exit__(self, type, value, tb):
        glEnd()


def draw_ellipse(x_radius, y_radius, z_radius, slices, stacks):
    glPushMatrix()
    glScalef(x_radius, y_radius, z_radius)
    glutSolidSphere(1, slices, stacks)
    glPopMatrix()


