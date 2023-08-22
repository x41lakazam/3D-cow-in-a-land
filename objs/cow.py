from utils import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from dataclasses import dataclass

from materials import Materials



from objs.base import BaseObj

@dataclass
class CowProps:
    body_len: int
    body_height: int
    body_width: int

    head_width: int
    head_height: int
    head_depth: int

    tail_length: int

    eyes_size: int
    eyes_space: int

    nose_size: int
    nose_space: int

    leg_length: int

class Cow(BaseObj):

    def __init__(self, props: CowProps):
        self.props = props
        self.head_theta = 0     # Y-axis rotation
        self.head_phi = 0       # Rotation around
        self.tail_theta = 0
        self.tail_phi = 0

    def tail_up(self):
        self.tail_phi = 10

    def tail_down(self):
        self.tail_phi = -10

    def turn_tail_left(self):
        self.tail_theta = -10

    def turn_tail_right(self):
        self.tail_theta = 10

    def turn_head_left(self, inc):
        self.head_theta = min(self.head_theta + inc, 90)

    def turn_head_right(self, inc):
        self.head_theta = max(self.head_theta - inc, -90)

    def head_up(self, inc):
        self.head_phi += inc
        self.head_phi = min(self.head_phi, 45)
        self.head_phi = max(self.head_phi, -45)

    def draw_body(self):
        # Draw the body
        Materials.cow_white()
        draw_ellipse(
            self.props.body_len,
            self.props.body_height,
            self.props.body_width,
            20, 20)

    def draw_head(self):
        Materials.cow_white()
        glPushMatrix()

        glTranslatef(
            self.props.body_len,
            self.props.body_height,
            0,
            0
        )
        glRotatef(self.head_phi, 0,0,1)
        glRotatef(self.head_theta, 0,1,0)

        draw_ellipse(
            self.props.head_width,
            self.props.head_height,
            self.props.head_depth,
            20, 20)

        # Draw ears
        Materials.cow_white()
        EAR_SPACE = self.props.head_depth/4

        glPushMatrix()
        glTranslatef(
            0.0,
            self.props.head_height/2,
            EAR_SPACE
        )
        draw_ellipse(
            0.1, 1, 0.1, 20,20
        )

        glTranslatef(0,0,-2*EAR_SPACE)
        draw_ellipse(
            0.1, 1, 0.1, 20,20
        )
        glPopMatrix()

        # Draw eyes
        Materials.cow_eyes()

        glPushMatrix()
        glTranslate(
            self.props.head_width,
            0.0,
            self.props.eyes_space,
        )
        draw_ellipse(self.props.eyes_size, self.props.eyes_size, self.props.eyes_size, 20, 20)

        glTranslate(0,0,-2*self.props.eyes_space)
        draw_ellipse(self.props.eyes_size, self.props.eyes_size, self.props.eyes_size, 20, 20)

        glPopMatrix()


        # Draw nose
        Materials.cow_nose()
        NOSE_SPACE = self.props.head_depth/3
        glPushMatrix()
        glTranslate(
            self.props.head_width,
            -self.props.head_height/3,
            self.props.nose_space,
        )
        draw_ellipse(self.props.nose_size, self.props.nose_size, self.props.nose_size, 20, 20)

        glTranslate(0,0,-2*self.props.nose_space)
        draw_ellipse(self.props.nose_size, self.props.nose_size, self.props.nose_size, 20, 20)

        glPopMatrix()

        glPopMatrix()

    def draw_tail(self):
        Materials.cow_white()
        glPushMatrix()
        glTranslatef(
            -self.props.body_len,
            self.props.body_height/3,
            0, 0
        )

        glRotatef(-30, 0,0,1)

        glRotatef(self.tail_phi, 0, 0, 1)
        glRotatef(self.tail_theta, 0, 1, 0)

        draw_ellipse(
            self.props.tail_length,
            0.1,
            0.1,
            20,20
        )

        glPopMatrix()

    def draw_legs(self):
        Materials.cow_white()
        # Front-right leg
        glPushMatrix()
        glTranslatef(
            self.props.body_len/2,
            -self.props.leg_length,
            self.props.body_width/2,
        )
        draw_ellipse(
            0.1,
            self.props.leg_length,
            0.1,
            20,20
        )
        glPopMatrix()

        # Front-left leg
        glPushMatrix()
        glTranslatef(
            self.props.body_len/2,
            -self.props.leg_length,
            -self.props.body_width/2,
        )
        draw_ellipse(
            0.1,
            self.props.leg_length,
            0.1,
            20,20
        )
        glPopMatrix()

        # Back-right leg
        glPushMatrix()
        glTranslatef(
            -self.props.body_len/2,
            -self.props.leg_length,
            self.props.body_width/2,
        )
        draw_ellipse(
            0.1,
            self.props.leg_length,
            0.1,
            20,20
        )
        glPopMatrix()

        # Back-left leg
        glPushMatrix()
        glTranslatef(
            -self.props.body_len/2,
            -self.props.leg_length,
            -self.props.body_width/2,
        )
        draw_ellipse(
            0.1,
            self.props.leg_length,
            0.1,
            20,20
        )
        glPopMatrix()


    def draw(self):
        self.draw_body()
        self.draw_head()
        self.draw_tail()
        self.draw_legs()

