from utils import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from dataclasses import dataclass
from materials import Materials


from objs.base import BaseObj

class Lamp(BaseObj):

    def __init__(self, radius=0.1, height=10):
        self.radius = radius
        self.height = height

    def draw(self):
        glPushMatrix()
        glRotatef(90, 1,0,0)

        Materials.metal()
        glutSolidCylinder(self.radius, self.height, 20, 20)

        Materials.lamp_bulb()
        glutSolidSphere(0.3,20,20)

        glPopMatrix()

