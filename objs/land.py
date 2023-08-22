import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from constants import *
from utils import GL_BEGIN
from objs.base import BaseObj
from materials import Materials

class Land(BaseObj):
    def __init__(self, size, acc=100):
        self.acc = acc
        self.size = size
        self.normals = [
            [ round(random.random(),2)  if random.random() > 0.90 else 0
             for i in range(acc) ]
            for j in range(acc)
        ]


    def draw(self):
        _step = 2*self.size / self.acc   # Size of a sub-quad

        glPushMatrix()
        Materials.land()

        for i in range(self.acc):
            for j in range(self.acc):
                _x0 = i*_step - self.size
                _y0 = j*_step - self.size
                _x1 = _x0 + _step
                _y1 = _y0 + _step

                with GL_BEGIN(GL_QUADS):
                    glNormal3f(self.normals[i][j], 1, self.normals[i][j])
                    #glNormal3f(0, 1, 0)
                    glVertex3f(_x0, 0, _y0)
                    glVertex3f(_x1, 0, _y0)
                    glVertex3f(_x1, 0, _y1)
                    glVertex3f(_x0, 0, _y1)

        glPopMatrix()
