import random
import numpy as np
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from constants import *
from utils import GL_BEGIN
from objs.land import Land
from objs.cow import Cow, CowProps
from objs.tree import Tree
from objs.lamp import Lamp
from objs.rocks import Rock
from objs.msg_box import MessageBox
from materials import Materials


CAMERA_MOTION_STEP = 2
CAMERA_ZOOM_STEP = 0.5
RENDER_RATE_MS = 100
COW_STEP = 3
COW_TURN_STEP = 10
COW_HEAD_STEP = 10
HELP_MSG_DURATION = 5000
LAND_SIZE = 100
LAND_ACC = 100

SKY_COLOR = np.array([0.5, 0.5, 0.7])

light_constants = [
    GL_LIGHT0,
    GL_LIGHT1,
    GL_LIGHT2,
    GL_LIGHT3,
    GL_LIGHT4,
    GL_LIGHT5,
    GL_LIGHT6,
    GL_LIGHT7
]


class Commands:
    CAMERA_UP = 'w'.encode('ascii')
    CAMERA_DOWN = 's'.encode('ascii')
    CAMERA_RIGHT = 'd'.encode('ascii')
    CAMERA_LEFT = 'a'.encode('ascii')
    CAMERA_ZOOM_OUT = 'o'.encode('ascii')
    CAMERA_ZOOM_IN = 'O'.encode('ascii')
    CAMERA_ROTATE_RIGHT = 'x'.encode('ascii')
    CAMERA_ROTATE_LEFT = 'z'.encode('ascii')
    CAMERA_ROTATE_UP = 'X'.encode('ascii')
    CAMERA_ROTATE_DOWN = 'Z'.encode('ascii')
    CAMERA_TOGGLE_COW_EYES = ' '.encode('ascii')

    COW_FORWARD = 'i'.encode('ascii')
    COW_BACKWARD = 'k'.encode('ascii')
    COW_LEFT = 'j'.encode('ascii')
    COW_RIGHT = 'l'.encode('ascii')

    COW_HEAD_UP = '1'.encode('ascii')
    COW_HEAD_DOWN = '2'.encode('ascii')
    COW_HEAD_LEFT = '3'.encode('ascii')
    COW_HEAD_RIGHT = '4'.encode('ascii')
    COW_TAIL_LEFT = 'v'.encode('ascii')
    COW_TAIL_RIGHT = 'b'.encode('ascii')
    COW_TAIL_UP = 'n'.encode('ascii')
    COW_TAIL_DOWN = 'm'.encode('ascii')

    LIGHT_BULB_THETA = ','.encode('ascii')
    LIGHT_BULB_PHI = '.'.encode('ascii')
    LIGHT_BULB_DEC_SPOT = '['.encode('ascii')
    LIGHT_BULB_INC_SPOT = ']'.encode('ascii')
    LIGHT_BULB_DEC_CUTOFF = '{'.encode('ascii')
    LIGHT_BULB_INC_CUTOFF = '}'.encode('ascii')
    LIGHT_BULB_DEC_EXPONENT = '('.encode('ascii')
    LIGHT_BULB_INC_EXPONENT = ')'.encode('ascii')
    LIGHT_BULB_DEC_INTENSITY = '<'.encode('ascii')
    LIGHT_BULB_INC_INTENSITY = '>'.encode('ascii')

    QUIT_MENU = 'q'.encode('ascii')

    @classmethod
    def get_summary(cls, sep="\n"):
        s = ""
        for attr in dir(cls):
            if attr.startswith("__") or hasattr(getattr(cls, attr), "__call__"):
                continue
            val = getattr(cls, attr).decode('ascii')
            if val == ' ':
                val = "SPACE"
            s += f"{attr}: {val}"
            s += sep

        return s



class Window:

    def __init__(self, land_size=100, land_acc=100, n_trees=30, n_rocks=50):
        # Window
        self.width, self.height = SIZE

        # Objects
        self.land = Land(land_size, land_acc)

        self.cow = Cow(
                CowProps(body_len=3, body_height=2, body_width=2,
                         head_width=1, head_depth=1, head_height=1,
                         tail_length=0.8, eyes_size=0.1, leg_length=1.3,
                        nose_size=0.05, eyes_space=0.3, nose_space=0.09)
            )

        self.trees = [
            (
                Tree(random.uniform(2,4)),
                [random.randint(-50,50), 0, random.randint(-50,50)]
            ) for _ in range(n_trees)
        ]
        self.rocks = [
            (
                Rock(random.uniform(1,6)),
                [random.randint(-50,50), 0, random.randint(-50,50)]
            ) for _ in range(n_rocks)
        ]

        # Cow props
        self.cow_pos = [0,0.8,0]
        self.cow_theta = 0

        # Camera props
        self.camera_distance = 2
        self.camera_pos = [-5,-3,0]
        self.camera_theta = 0  # rotation around y-axis (horizon)
        self.camera_phi = 0    # rotation around x-axis

        # States
        self.see_through_cow_eyes = False
        self.display_help_message = False
        self.help_msg = Commands.get_summary()
        self.help_msg_font = GLUT_BITMAP_TIMES_ROMAN_24


        # Light props
        self.ambient_light_intensity = 1
        self.light_bulb_intensity = 1
        self.light_bulb_spot_exponent = 50
        self.light_bulb_theta = 60
        self.light_bulb_phi = -90
        self.light_bulb_cutoff = 45

        self.lamps = [
            (Lamp(), [2,0,7], GL_LIGHT1),
            (Lamp(), [6,0,-4], GL_LIGHT2),
            (Lamp(), [-2,0,-3], GL_LIGHT3),
        ]
        self.lamps.extend([
            (
                Lamp(),
                [
                    random.randint(-land_size//2, land_size//2),
                    0,
                    random.randint(-land_size//2, land_size//2)
                ],
                LIGHT
            ) for LIGHT in light_constants[3:]
        ])

    def set_camera_pos(self, eye_pos, ref_pos, up_vec):
        """Wraps gluLookAt"""
        gluLookAt(*eye_pos, *ref_pos, *up_vec)

    def init_light(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, [1,1,1,1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.33, 0.808, 0.980,1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0,0,0,1])
        glLightfv(GL_LIGHT0, GL_POSITION, [2,2,2,1])

    def initGL(self):
        self.init_light()
        glClearColor(*SKY_COLOR, 1.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)

    def draw(self):
        """Draw main scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glClearColor(*(SKY_COLOR*self.ambient_light_intensity), 1.0)
        glPushMatrix()

        # Camera pos: can be cow POV or global camera
        if self.see_through_cow_eyes:
            yaw = (self.cow_theta + self.cow.head_theta) % 360

            pitch = 0
            # Calculate direction using sphere parametric equation
            direction = np.array([
                np.cos(np.radians(yaw)) * np.cos(np.radians(pitch)),
                np.sin(np.radians(pitch)),
                np.sin(np.radians(yaw)) * np.cos(np.radians(pitch))
            ])
            direction /= np.linalg.norm(direction)


            cow_eyes = [
                self.cow_pos[0],
                3,
                self.cow_pos[2]
            ]

            self.set_camera_pos(
                cow_eyes,
                cow_eyes+direction,
                (0,1,0)
            )
        else:
            glTranslatef(*self.camera_pos)
            glRotatef(self.camera_theta, 0, 1, 0)
            glRotatef(self.camera_phi, 1,0,0)
            glScalef(1/self.camera_distance,1/self.camera_distance, 1/self.camera_distance)


        # Draw objects
        if not self.see_through_cow_eyes:
            self.draw_cow()

        self.land.draw()
        self.draw_trees()
        self.draw_rocks()
        self.draw_lamps()

        if self.display_help_message:
            self.draw_help_message()

        glPopMatrix()

        glutSwapBuffers()  # Add this line

    def draw_help_message(self):
        """Display a message with all the commands"""
        # Disable lighting and enter model view mode
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)

        glPushMatrix()
        glLoadIdentity()

        # Draw text
        raster_y = (self.height // 2) - 600
        glColor3f(0,0,0)  # Set the text color
        for line in self.help_msg.split("\n"):
            raster_x = 100
            for char in line:
                glRasterPos2f(raster_x, raster_y)
                glutBitmapCharacter(self.help_msg_font, ord(char))
                raster_x += 20
            raster_y += 40

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_LIGHTING)

    def draw_cow(self):
        """Position the cow and draw it"""
        glPushMatrix()
        glTranslatef(*self.cow_pos)
        glRotatef(self.cow_theta, 0,1,0)
        glScalef(0.3, 0.3, 0.3)
        self.cow.draw()
        glPopMatrix()

    def draw_lamps(self):

        # Light properties

        r = self.light_bulb_intensity
        ambient_light = [0.1*r, 0.1*r, 0.1*r, 1]
        diffuse_light = [1.0*r, 0.95*r, 0.8*r, 1]  # Slightly yellowish for warmth
        specular_light = [1*r, 1*r, 1*r, 1*r]  # Bright white specular reflection
        phi = np.radians(self.light_bulb_phi)
        theta = np.radians(self.light_bulb_theta)
        spot_direction = [np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)]
        spot_exponent = self.light_bulb_spot_exponent
        spot_cutoff = self.light_bulb_cutoff
        constant_attenuation = 1.0
        linear_attenuation = 0.05
        quadratic_attenuation = 0.01

        for lamp, coords, light in self.lamps:
            # Draw the lamp
            glPushMatrix()
            coords[1] = lamp.height/2
            glTranslatef(*coords)
            lamp.draw()
            glPopMatrix()

            # Add point light
            glEnable(light)

            glLightfv(light, GL_DIFFUSE, diffuse_light)
            glLightfv(light, GL_SPECULAR, specular_light)
            glLightfv(light, GL_SPOT_DIRECTION, spot_direction)
            glLightfv(light, GL_SPOT_EXPONENT, spot_exponent)
            glLightfv(light, GL_SPOT_CUTOFF, spot_cutoff)
            glLightfv(light, GL_CONSTANT_ATTENUATION, constant_attenuation)
            glLightfv(light, GL_LINEAR_ATTENUATION, linear_attenuation)
            glLightfv(light, GL_QUADRATIC_ATTENUATION, quadratic_attenuation)
            glLightfv(light, GL_POSITION, [coords[0], coords[1], coords[2],1])

    def draw_rocks(self):
        for rock, coords in self.rocks:
            glPushMatrix()
            glTranslatef(*coords)
            rock.draw()
            glPopMatrix()

    def draw_trees(self):
        for tree, coords in self.trees:
            glPushMatrix()
            coords[1] = tree.size/2
            glTranslatef(*coords)
            tree.draw()
            glPopMatrix()


    def keyboard(self, key, x, y):
        if key in (Commands.CAMERA_UP, Commands.CAMERA_DOWN, Commands.CAMERA_RIGHT, Commands.CAMERA_LEFT):
            self._move_camera(key)

        elif key == Commands.CAMERA_ZOOM_IN:
            self._camera_zoom_in()

        elif key == Commands.CAMERA_ZOOM_OUT:
            self._camera_zoom_out()

        elif key == Commands.CAMERA_ROTATE_LEFT:
            if self.see_through_cow_eyes:
                return # Forbidden
            self.camera_theta = (self.camera_theta + 10) % 360

        elif key == Commands.CAMERA_ROTATE_UP:
            if self.see_through_cow_eyes:
                return # Forbidden
            self.camera_phi = (self.camera_phi - 10) % 360

        elif key == Commands.CAMERA_ROTATE_DOWN:
            if self.see_through_cow_eyes:
                return # Forbidden
            self.camera_phi = (self.camera_phi + 10) % 360


        elif key == Commands.CAMERA_ROTATE_RIGHT:
            if self.see_through_cow_eyes:
                return # Forbidden
            self.camera_theta = (self.camera_theta - 10) % 360

        elif key == Commands.CAMERA_TOGGLE_COW_EYES:
            self.see_through_cow_eyes ^= True

        elif key in (Commands.COW_FORWARD, Commands.COW_BACKWARD):
            self._move_cow(key)

        elif key in (Commands.COW_RIGHT, Commands.COW_LEFT):
            self._turn_cow(key)

        elif key == Commands.COW_HEAD_LEFT:
            self.cow.turn_head_left(COW_HEAD_STEP)

        elif key == Commands.COW_HEAD_RIGHT:
            self.cow.turn_head_right(COW_HEAD_STEP)

        elif key == Commands.COW_HEAD_UP:
            self.cow.head_up(COW_HEAD_STEP)

        elif key == Commands.COW_HEAD_DOWN:
            self.cow.head_up(-COW_HEAD_STEP)

        elif key == Commands.COW_TAIL_LEFT:
            self.cow.turn_tail_left()

        elif key == Commands.COW_TAIL_RIGHT:
            self.cow.turn_tail_right()

        elif key == Commands.COW_TAIL_UP:
            self.cow.tail_up()

        elif key == Commands.COW_TAIL_DOWN:
            self.cow.tail_down()

        elif key == Commands.LIGHT_BULB_PHI:
            self.light_bulb_phi = (self.light_bulb_phi + 10) % 360

        elif key == Commands.LIGHT_BULB_THETA:
            self.light_bulb_theta = (self.light_bulb_theta + 10) % 360

        elif key == Commands.LIGHT_BULB_DEC_SPOT:
            self.light_bulb_spot_exponent -= 1

        elif key == Commands.LIGHT_BULB_INC_SPOT:
            self.light_bulb_spot_exponent += 1

        elif key == Commands.LIGHT_BULB_DEC_EXPONENT:
            self.light_bulb_spot_exponent = max(self.light_bulb_spot_exponent - 10, 0)

        elif key == Commands.LIGHT_BULB_INC_EXPONENT:
            self.light_bulb_spot_exponent += 10

        elif key == Commands.LIGHT_BULB_DEC_CUTOFF:
            self.light_bulb_cutoff = max(self.light_bulb_cutoff - 10, 0)

        elif key == Commands.LIGHT_BULB_INC_CUTOFF:
            self.light_bulb_cutoff = min(self.light_bulb_cutoff + 10, 90)

        elif key == Commands.LIGHT_BULB_DEC_INTENSITY:
            self.light_bulb_intensity = max(self.light_bulb_intensity-0.2, 0)

        elif key == Commands.LIGHT_BULB_INC_INTENSITY:
            self.light_bulb_intensity += 0.2

        elif key == Commands.QUIT_MENU:
            self.display_help_message = False

    def _camera_zoom_out(self):
        if self.see_through_cow_eyes:
            return # Forbidden

        self.camera_distance += CAMERA_ZOOM_STEP

    def _camera_zoom_in(self):
        if self.see_through_cow_eyes:
            return # Forbidden

        self.camera_distance -= CAMERA_ZOOM_STEP
        if self.camera_distance <= 0:
            self.camera_distance = 0.3

    def _move_cow(self, key):
        direction = 1 if key == Commands.COW_FORWARD else -1
        self.cow_pos[0] += COW_STEP*np.cos(np.radians(self.cow_theta))*direction
        self.cow_pos[2] += COW_STEP*np.sin(np.radians(self.cow_theta))*-direction

    def _turn_cow(self, key):
        direction = 1 if key == Commands.COW_LEFT else -1
        self.cow_theta += COW_TURN_STEP*direction
        self.cow_theta %= 360

    def _move_camera(self, key):
        if self.see_through_cow_eyes:
            return # Forbidden

        if key in (Commands.CAMERA_UP, Commands.CAMERA_DOWN):
            self._move_camera_vertically(-1 if key == Commands.CAMERA_UP else 1)
        else:
            self._move_camera_horizontally(-1 if key == Commands.CAMERA_RIGHT else 1)

    def _move_camera_horizontally(self, direction):
        """direction=1 for right and -1 for left"""
        self.camera_pos[0] += direction*CAMERA_MOTION_STEP*np.cos(np.radians(self.camera_theta))
        self.camera_pos[2] += direction*CAMERA_MOTION_STEP*np.sin(np.radians(self.camera_theta))

    def _move_camera_vertically(self, direction):
        """direction=1 for up and -1 for down"""
        self.camera_pos[1] += direction*CAMERA_MOTION_STEP

    def reshape(self, width, height):
        h = float(height) / float(width);
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, 1.0, -h, h, 5.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -40.0)
        self.width = width
        self.height = height

    def timer(self, v):
        glutPostRedisplay()
        glutTimerFunc(RENDER_RATE_MS, self.timer, 1)

    def process_menu_events(self, val):
        if val == 1: # help
            self.display_help_message = True

        return 0

    def adjust_ambient_light_intensity(self, light):
        light = max(light, 0)
        light = min(light, 10)
        light /= 10
        self.ambient_light_intensity = light
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (light, light, light, 1))
        print("Ambient light changed to", light)

    def adjust_local_light_intensity(self, light):
        """Adjust the intensity of the light bulbs"""
        light = max(light, 0)
        light = min(light, 10)
        light /= 10
        self.light_bulb_intensity = light
        print("Local light changed to", light)


    def create_menu(self):
        local_light_intensity_menu = glutCreateMenu(self.adjust_local_light_intensity)
        for i in range(11):
            glutAddMenuEntry(str(i), i)

        light_intensity_menu = glutCreateMenu(self.adjust_ambient_light_intensity)
        for i in range(11):
            glutAddMenuEntry(str(i), i)

        menu = glutCreateMenu(self.process_menu_events)
        glutAddMenuEntry("Help", 1)
        glutAddSubMenu("Adjust global light intensity", light_intensity_menu)
        glutAddSubMenu("Adjust bulbs intensity", local_light_intensity_menu)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
        # Add the following line to fix your code
        return 0

    # Cow tail periodic moves
    def cow_tail_move_1(self, v):
        print("MOVE")
        self.cow.turn_tail_left()
        glutTimerFunc(500, self.cow_tail_move_2, 1)

    def cow_tail_move_2(self, v):
        self.cow.turn_tail_right()
        glutTimerFunc(500, self.cow_tail_move_3, 1)

    def cow_tail_move_3(self, v):
        self.cow.turn_tail_left()
        glutTimerFunc(random.randint(1000, 5000), self.cow_tail_move_1, 1)
    #   --------

    def run(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

        glutInitWindowPosition(0, 0)
        glutInitWindowSize(self.width, self.height)
        self.id = glutCreateWindow(TITLE)
        self.initGL()

        glutKeyboardFunc(self.keyboard)
        glutDisplayFunc(self.draw)
        glutReshapeFunc(self.reshape)
        glutTimerFunc(RENDER_RATE_MS, self.timer, 1)
        # Periodically move the tail of the cow, its cute
        glutTimerFunc(1000, self.cow_tail_move_1, 1)
        self.create_menu()

        glutMainLoop()


if __name__ == "__main__":
    Window(land_size=LAND_SIZE, land_acc=LAND_ACC, n_trees=30, n_rocks=50).run()
