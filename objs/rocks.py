import random
from utils import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from dataclasses import dataclass


from materials import Materials
from objs.base import BaseObj

class Rock(BaseObj):

    def __init__(self, size):
        self.size = size
        self.rotation = random.randint(0,90)
        self.rotation_axis = [
            random.randint(0,1),
            random.randint(0,1),
            random.randint(0,1),
        ]

    def draw(self):
        glPushMatrix()

        # Draw trunk
        Materials.rock()
        glScale(self.size*0.05, self.size*0.05, self.size*0.05)
        glRotatef(self.rotation, *self.rotation_axis)
        glutSolidDodecahedron()

        glPopMatrix()

