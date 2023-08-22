import random
from utils import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from dataclasses import dataclass


from materials import Materials
from objs.base import BaseObj

class Tree(BaseObj):

    def __init__(self, size):
        self.size = size
        self.leaves_size_x = random.randint(3,7)
        self.leaves_size_z = random.randint(2,6)

    def draw(self):
        glPushMatrix()

        # Draw trunk
        Materials.tree()
        glScale(0.2, self.size, 0.3)
        glutSolidDodecahedron()

        # Draw leaves
        glTranslatef(0, self.size/2, 0)
        Materials.leaves()
        glScale(self.leaves_size_x, 0.7, self.leaves_size_z)
        glutSolidDodecahedron()


        glPopMatrix()

