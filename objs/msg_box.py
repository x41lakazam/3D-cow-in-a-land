from utils import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from dataclasses import dataclass

from materials import Materials

from objs.base import BaseObj


class MessageBox(BaseObj):
    def __init__(self, message, font=GLUT_BITMAP_TIMES_ROMAN_24):
        self.message = message
        self.font = font

    def draw(self):
        glutPushWindow()
        glClear(GL_COLOR_BUFFER_BIT)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.5, 0.5, 0.5, 1])
        glColor3f(0.5, 0.5, 0.5)
        #glEnable(GL_BLEND);
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);


        glBegin(GL_POLYGON)
        glVertex2f(-400.0, -400.0)
        glVertex2f(400.0, -400.0)
        glVertex2f(400.0, 400.0)
        glVertex2f(-400.0, 400.0)
        glEnd()

        #glDisable(GL_BLEND);

        # raster_y = 0
        # for line in self.message.split("\n"):
        #     glRasterPos2f(0, raster_y)
        #     glutBitmapString(self.font, line.encode('utf-8'))
        #     raster_y -= 0.5

        # Draw a gray rectangle
        #glRectf()
