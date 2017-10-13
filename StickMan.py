from OpenGL.GL import *
import numpy as np
import math

import Cursor
import Events
import Graphics
import Definitions
import Sensors
import Shaders


class characteristics(object):
    """
        characteristics
        .o      rotation angle
        .xyz    rotation axis
    """
    __name__ = "characteristics"
    nb__init__ = 0 # keeps track of how many creations there are


    def __init__(self, ini = 1.70, coord = (0, 0, 0), parts = []): # add orientation sometime...
        """ constructor """
        characteristics.nb__init__ += 1
        self.size = ini # change to a 3D scale after ?
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        self.parts = parts

    @classmethod
    def feedback(cls,reset = False):
        """ print feedback on class calls """
        print("nb__init__ : {}".format(characteristics.nb__init__))
        if reset == True:
            characteristics.nb__init__ = 0
            print("reset for {} is done".format(cls.__name__))
        print("\n")
        

    def values(self):
        """ print characteristics values """
        print(self.size, self.x, self.y, self.z)
        for p in self.parts:
            print(p)

            
selectedParts = []
virtuMan = None

def preprocessPart(x,y,z,dx,dy,dz,partIsSelected, ID):

    """ part transformations """
    Definitions.transform.push()
    Definitions.transform.translate(dx,dy,dz)
    Definitions.transform.scale(x,y,z)
    
    """ store transformation in package """
    Definitions.packageStickMan = Definitions.packageStickMan + [[Definitions.transform.peek(), partIsSelected, ID],]

    Definitions.transform.pop()


def drawStickMan(style):
    """ send color to shader """
    glUniform4fv(Shaders.setColor_loc, 1, np.array([1.,1.,1.,0.3], dtype = np.float32))
    """ choose vbo """
    vboId = Graphics.vboCube
    """ bind surfaces vbo """
    Graphics.indexPositions[vboId][Graphics.vboSurfaces].bind()
    Graphics.vertexPositions[vboId].bind()
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
    """ draw all at once """
    i = 0
    for pack in Definitions.packageStickMan:
        i +=1./len(Definitions.packageStickMan)
        if pack[1] == True:
            glUniform4fv(Shaders.setColor_loc, 1, np.array([0.,0.,1.,0.3], dtype = np.float32))
        if style == 3:
            glUniform4fv(Shaders.setColor_loc, 1, np.array([i,0.,0.,1.], dtype = np.float32))
        glUniformMatrix4fv(Shaders.transform_loc, 1, GL_FALSE, pack[0])
        """ draw vbo """
        glDrawElements(Graphics.styleIndex[vboId][Graphics.vboSurfaces], Graphics.nbIndex[vboId][Graphics.vboSurfaces], GL_UNSIGNED_INT, None)
        if pack[1] == True:
            glUniform4fv(Shaders.setColor_loc, 1, np.array([1.,1.,1.,0.3], dtype = np.float32))

    
    """ send color to shader """
    if style == Graphics.opaque:
        glUniform4fv(Shaders.setColor_loc, 1, np.array([0.5,0.5,0.5,1.], dtype = np.float32))
    elif style == Graphics.blending:
        glUniform4fv(Shaders.setColor_loc, 1, np.array([1.,1.,1.,1.], dtype = np.float32))
    if style == Graphics.opaque or style == Graphics.blending:
        """ bind edges vbo """
        Graphics.indexPositions[vboId][Graphics.vboEdges].bind()
        Graphics.vertexPositions[vboId].bind()
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        """ draw all at once """
        for pack in Definitions.packageStickMan:
            glUniformMatrix4fv(Shaders.transform_loc, 1, GL_FALSE, pack[0])
            """ draw vbo """
            glDrawElements(Graphics.styleIndex[vboId][Graphics.vboEdges], Graphics.nbIndex[vboId][Graphics.vboEdges], GL_UNSIGNED_INT, None)

            

part = -1 # global helps through recursivity
""" recursive function that goes through all body parts and sensors """
def stick(entity = characteristics(), offset = (0,0,0), rotation = (0,0,0,0)):
    global part
    global selectedPart
    if part + 1 >= len(entity.parts):
        return

    part += 1
    current_part = part

    """ Check if part is selected """
    partIsSelected = False
    for selectedPart in selectedParts:
        if selectedPart == entity.parts[current_part][Data_id]:
            partIsSelected = True
            break


    """ default orientation of part """
    l = Definitions.vector4D.Eul2Quat(Definitions.vector4D((0, entity.parts[current_part][Data_angleRepos][0], entity.parts[current_part][Data_angleRepos][1], entity.parts[current_part][Data_angleRepos][2])))

    """ current rotation of part """
    m = Definitions.vector4D((entity.parts[current_part][Data_angle]))
    
    """ resulting orientation of part """
    q = m

    """ new rotation to implement """
    n = Definitions.vector4D.Eul2Quat(Definitions.vector4D((0, 0, 0, 0)))
    if partIsSelected == True:
        """ the rotation command """
        n = Definitions.vector4D.Eul2Quat(Definitions.vector4D((0, Events.pivot[0], Events.pivot[1], Events.pivot[2])))

        """ resulting orientation of part ... """
        q = Definitions.vector4D.QuatProd(m,n)

        """ ... with saturations """
        q = Definitions.vector4D.QuatSat(q, (entity.parts[current_part][Data_saturation]))

        """ store resulting orientation """
        entity.parts[current_part][Data_angle] = [q.o,q.x,q.y,q.z]
    

    """ Transformations """
    glPushMatrix()
    Definitions.transform.push()
    """ offset to apply """
    glTranslatef(offset[0] + entity.size*entity.parts[current_part][Data_offset][0], offset[1] + entity.size*entity.parts[current_part][Data_offset][1], offset[2] + entity.size*entity.parts[current_part][Data_offset][2])
    Definitions.transform.translate(offset[0] + entity.size*entity.parts[current_part][Data_offset][0], offset[1] + entity.size*entity.parts[current_part][Data_offset][1], offset[2] + entity.size*entity.parts[current_part][Data_offset][2])
    """ total rotation to apply """
    p = Definitions.vector4D.Quat2Vec(Definitions.vector4D.QuatProd(l,q))
    if math.sqrt(p.x*p.x + p.y*p.y + p.z*p.z) >= 0.0001:
        glRotatef(p.o, p.x, p.y, p.z)
        Definitions.transform.rotate(p.o, p.x, p.y, p.z)
        
        
    """ preprocess part """
    x = entity.size*entity.parts[current_part][Data_dimensions][0]
    y = entity.size*entity.parts[current_part][Data_dimensions][1]
    z = entity.size*entity.parts[current_part][Data_dimensions][2]
    dx = 0.5*entity.size*entity.parts[current_part][Data_dimensions][0]
    dy = 0
    dz = 0
    preprocessPart(x,y,z,dx,dy,dz,partIsSelected, entity.parts[current_part][Data_id])

    """ preprocess sensors """
    for sensor in Sensors.virtuSens:
        if sensor.attach == entity.parts[current_part][Data_id]:
            sensor.h = 0.707*max(entity.size*entity.parts[current_part][Data_dimensions][1],entity.size*entity.parts[current_part][Data_dimensions][2])
            """ store transformation in package """
            Definitions.packageSensors = Definitions.packageSensors + [[Definitions.transform.peek(), sensor],]


    """ recursive call for all parts attached to the current one """
    while part + 1 < len(entity.parts) and entity.parts[part+1][Data_layer] > entity.parts[current_part][Data_layer]:
        stick(entity, (x, 0, 0), (0,0,0,0))

    glPopMatrix()
    Definitions.transform.pop()



fi_a = 0.0323
fi_b = 0.0153
fi_c = 0.0141
"""
    0 - id : char string
    1 - offset x,y,z : ratio of characteristics.size
    2 - dimensions x,y,z : ratio of characteristics.size
    3 - saturation x+, x-, y+,y- ,z+ ,z- : degrees [180;-180]
    4 - angleRepos x,y,z : degrees
    5 - angle x,y,z : quaternion. (NOTE : it is not possible to convert back to euler angles so we stay in quaternion form here. anyways it would require more computation as well.)
    6 - layer : if layer(p+1) > layer(p), build from part(p). else close part(p) and repeat while a part is open.
    Note : the Torse shares it's saturations with the Wrist. To move the Wrist, move instead the Torse + Origin
"""
Data_id = 0
Data_offset = 1
Data_dimensions = 2
Data_saturation = 3
Data_angleRepos = 4
Data_angle = 5
Data_layer = 6
parts = [
    ["Origin",          [0, 0, 0],          [0., 0., 0.],                 [180, -180, 180, -180, 180, -180],   [0, 0, 90],         [1, 0, 0, 0],          0],
    ["Wrist",           [0, 0, 0],          [0.191, 0.15, 0.05],          [0, 0, 0, 0, 0, 0],                  [0, 0, 180],        [1, 0, 0, 0],          1],
    ["Upp_leg_r",       [0, 0.075, 0],      [0.195, 0.1, 0.1],            [45, -45, 0, -150, 30, -30],          [0, 0, 0],          [1, 0, 0, 0],          2],
    ["Low_leg_r",       [0, 0, 0],          [0.246, 0.08, 0.08],          [45, -45, 150, 0, 0, 0],             [0, 0, 0],          [1, 0, 0, 0],          3],
    ["Feet_r",          [0, 0, 0],          [0.0882, 0.0588, 0.02],       [5, -15, 60, -15, 0, 0],             [0, -90, 0],        [1, 0, 0, 0],          4],
    ["Upp_leg_l",       [0, -0.075, 0],     [0.195, 0.1, 0.1],            [45, -45, 0, -150, 30, -30],          [0, 0, 0],          [1, 0, 0, 0],          2],
    ["Low_leg_l",       [0, 0, 0],          [0.246, 0.08, 0.08],          [45, -45, 150, 0, 0, 0],             [0, 0, 0],          [1, 0, 0, 0],          3],
    ["Feet_l",          [0, 0, 0],          [0.0882, 0.0588, 0.02],       [15, -5, 60, -15, 0, 0],             [0, -90, 0],        [1, 0, 0, 0],          4],
    ["Torse",           [0, 0, 0],          [0.169, 0.15, 0.05],          [15, -15, 30, -60, 45, -45],         [0, 0, 0],          [1, 0, 0, 0],          1],
    ["Neck",            [0, 0, 0],          [0.052, 0.03, 0.03],          [0, 0, 15, -60, 30, -30],            [0, 0, 0],          [1, 0, 0, 0],          2],
    ["Head",            [0, 0, 0],          [0.130, 0.08, 0.08],          [60, -60, 30, -30, 15, -15],         [0, 0, 0],          [1, 0, 0, 0],          3],
    ["Shoulder_r",      [0, 0, 0],          [0.106, 0.04, 0.04],          [15, -15, 15, -15, 15, -15],             [0, 0, 90],         [1, 0, 0, 0],          2],
    ["Arm_r",           [0, 0, 0],          [0.136, 0.06, 0.06],          [0, -90, 60, -60, 90, 0],            [0, 0, 0],          [1, 0, 0, 0],          3],
    ["Forearm_r",       [0, 0, 0],          [0.146, 0.04, 0.04],          [90, -90, 0, -150, 0, 0],            [0, 0, 0],          [1, 0, 0, 0],          4],
    ["Hand_r",          [0, 0, 0],          [0.0588, 0.06, 0.02],         [0, 0, 90, -90, 15, -15],            [0, 0, 5],          [1, 0, 0, 0],          5],
    ["Finger_r_1a",     [-0.04, -0.03, 0],  [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, -30],        [1, 0, 0, 0],          6],
    ["Finger_r_1b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_r_1c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8],
    ["Finger_r_2a",     [0, -0.03, 0],      [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, -15],        [1, 0, 0, 0],          6],
    ["Finger_r_2b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_r_2c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8],
    ["Finger_r_3a",     [0, -0.01, 0],      [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, -5],         [1, 0, 0, 0],          6],
    ["Finger_r_3b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_r_3c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8],
    ["Finger_r_4a",     [0, 0.01, 0],       [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, 5],          [1, 0, 0, 0],          6],
    ["Finger_r_4b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_r_4c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8],
    ["Finger_r_5a",     [0, 0.03, 0],       [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, 15],         [1, 0, 0, 0],          6],
    ["Finger_r_5b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_r_5c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8],
    ["Shoulder_l",      [0, 0, 0],          [0.106, 0.04, 0.04],          [15, -15, 15, -15, 15, -15],             [0, 0, -90],        [1, 0, 0, 0],          2],
    ["Arm_l",           [0, 0, 0],          [0.136, 0.06, 0.06],          [90, 0, 60, -60, 0, -90],            [0, 0, 0],          [1, 0, 0, 0],          3],
    ["Forearm_l",       [0, 0, 0],          [0.146, 0.04, 0.04],          [90, -90, 0, -150, 0, 0],            [0, 0, 0],          [1, 0, 0, 0],          4],
    ["Hand_l",          [0, 0, 0],          [0.0588, 0.06, 0.02],         [0, 0, 90, -90, 15, -15],            [0, 0, -5],         [1, 0, 0, 0],          5],
    ["Finger_l_1a",     [-0.04, 0.03, 0],   [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, 30],         [1, 0, 0, 0],          6],
    ["Finger_l_1b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_l_1c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8],
    ["Finger_l_2a",     [0, 0.03, 0],       [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, 15],         [1, 0, 0, 0],          6],
    ["Finger_l_2b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_l_2c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8],
    ["Finger_l_3a",     [0, 0.01, 0],       [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, 5],          [1, 0, 0, 0],          6],
    ["Finger_l_3b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_l_3c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8],
    ["Finger_l_4a",     [0, -0.01, 0],      [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, -5],         [1, 0, 0, 0],          6],
    ["Finger_l_4b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_l_4c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8],
    ["Finger_l_5a",     [0, -0.03, 0],      [fi_a, 0.01, 0.01],           [0, 0, 0, -90, 10, -10],             [0, 0, -15],        [1, 0, 0, 0],          6],
    ["Finger_l_5b",     [0, 0, 0],          [fi_b, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          7],
    ["Finger_l_5c",     [0, 0, 0],          [fi_c, 0.01, 0.01],           [0, 0, 0, -90, 0, 0],                [0, 0, 0],          [1, 0, 0, 0],          8]
    ]