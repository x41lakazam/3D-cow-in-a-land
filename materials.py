from utils import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Materials:

    @staticmethod
    def cow_white():
        cow_white_ambient = [0.7, 0.7, 0.7, 1.0]
        cow_white_diffuse = [1.0, 1.0, 1.0, 1.0]
        cow_white_specular = [0.2, 0.2, 0.2, 1.0]

        glMaterialfv(GL_FRONT, GL_AMBIENT, cow_white_ambient);
        glMaterialfv(GL_FRONT, GL_SPECULAR, cow_white_specular);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, cow_white_diffuse);
        glMaterialfv(GL_FRONT, GL_SHININESS, [0]);

    @staticmethod
    def cow_eyes():
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0]);
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0]);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0, 0, 0, 1.0]);

    @staticmethod
    def cow_nose():
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 1.0]);
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1.0]);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0, 0, 0, 1.0]);

    @staticmethod
    def land():
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.113, 0.247, 0.014, 1.0]);
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.42, 0.557, 0.137, 1.0]);
        glMaterialfv(GL_FRONT, GL_DIFFUSE,[0.03, 0.03, 0.03, 1.0] );
        glMaterialfv(GL_FRONT, GL_SHININESS, [30]);

    @staticmethod
    def tree():
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.49, 0.33, 0.013, 1.0]);
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.24, 0.94, 0.16, 1.0] );
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.04, 0.04, 0.04, 1.0]);
        glMaterialfv(GL_FRONT, GL_SHININESS, [50]);

    @staticmethod
    def leaves():
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.113, 0.447, 0.014, 1.0]);
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.42, 0.357, 0.137, 1.0]);
        glMaterialfv(GL_FRONT, GL_DIFFUSE,[0.03, 0.03, 0.03, 1.0] );
        glMaterialfv(GL_FRONT, GL_SHININESS, [0]);

    @staticmethod
    def lamp_bulb():
        ambient_light = [0.8, 0.8, 0.8, 1]
        diffuse_light = [0.9, 0.9, 0.6, 1]  # Slightly yellowish for warmth
        specular_light = [1, 1, 1, 1]  # Bright white specular reflection
        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_light);
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular_light);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_light);
        glMaterialfv(GL_FRONT, GL_SHININESS, [0]);

    @staticmethod
    def metal():
        ambient_light = [0.2125,	0.1275,	0.054, 1]
        diffuse_light = [0.714,	0.4284,	0.18144 , 1]  # Slightly yellowish for warmth
        specular_light = [0.393548, 	0.271906, 	0.166721 , 1]  # Bright white specular reflection

        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.19225, 0.19225, 0.19225, 1.0]);
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.508273, 0.508273, 0.508273, 1.0]);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.50754, 0.50754, 0.50754, 1.0]);
        glMaterialfv(GL_FRONT, GL_SHININESS, [20]);


    @staticmethod
    def rock():
        rock_ambient = [0.68, 0.69, 0.60, 1.0]

        rock_diffuse = [0.68, 0.69, 0.60, 1.0]
        rock_specular = [0.1, 0.1, 0.1, 1.0]
        rock_shininess = [10.0]

        glMaterialfv(GL_FRONT, GL_AMBIENT, rock_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, rock_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, rock_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, rock_shininess)

