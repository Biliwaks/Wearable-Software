class muscle(object):
    """
        muscle
    """

    def __init__(self): # add orientation sometime...
        """ constructor """
        self.id = 0
        self.tag = ''
        self.A = ""
        self.Alocal = []
        self.Aworld = []
        self.B = ""
        self.Blocal = []
        self.Bworld = []
        self.modelMatrix = []


from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

import Definitions
import Graphics
import ID
import Sensors
import Shaders

def preprocessMuscle(entity):
    for i in range(0,len(entity.muscles)):

        P1 = entity.muscles[i].Aworld
        P2 = entity.muscles[i].Bworld
        if P1 == [] or P2 == []:
            continue

        v1 = Definitions.vector4D((0, 1, 0, 0))
        v2 = Definitions.vector4D((0, P1[0][0]-P2[0][0], P1[0][1]-P2[0][1], P1[0][2]-P2[0][2]))
        scale = math.sqrt(v2.x*v2.x + v2.y*v2.y + v2.z*v2.z)
        center = Definitions.vector4D((0, 0.5*(P1[0][0]+P2[0][0]), 0.5*(P1[0][1]+P2[0][1]), 0.5*(P1[0][2]+P2[0][2])))
        u = Definitions.vector4D.AngleAxisBetween2Vec(v1,v2)
    
        """ load matrix in shader """
        Definitions.modelMatrix.push()
        Definitions.modelMatrix.set(Definitions.I)
        Definitions.modelMatrix.translate(center.x, center.y, center.z)
        Definitions.modelMatrix.rotate(u.o, u.x, u.y, u.z)
        Definitions.modelMatrix.scale(scale,0.03,0.03)
        
        entity.muscles[i].modelMatrix = Definitions.modelMatrix.peek()

        
        for sensor in Sensors.virtuSens + Sensors.zoiSens:
            if sensor.attach == entity.muscles[i].tag:
                sensor.h = 0.6
                if sensor.type == 'Eye':
                    sensor.h = 0.4
                if ID.idCategory(sensor.id) == ID.ZOI:
                    sensor.h = 0.55
                Sensors.preprocessSensor(sensor, scale, 0.03, 0.03)
        Definitions.modelMatrix.pop()

OverMuscId = 0
SelectedMuscId = 0

def drawMuscleSurface(entity, style):

    for i in range(0,len(entity.muscles)):

        """ verify matrix validity """
        if entity.muscles[i].modelMatrix == []:
            continue


        """ choose vbo """
        vboId = Graphics.vboHexagon
        vboDraw = Graphics.vboSurfaces
        """ bind surfaces vbo """
        Graphics.indexPositions[vboId][vboDraw].bind()
        Graphics.vertexPositions[vboId].bind()
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        
        """ choose color """
        if style == Graphics.idBuffer:
            r, g, b = ID.id2color(entity.muscles[i].id)
            color = np.array([r/255.,g/255.,b/255.,1.], dtype = np.float32)
        elif i+ID.offsetId(ID.MUSCLE) == SelectedMuscId:
            color = np.array([0.5,0,0.,0.3], dtype = np.float32)
        elif i+ID.offsetId(ID.MUSCLE) == OverMuscId:
            color = np.array([1,0,0,0.3], dtype = np.float32)
        else:
            color = np.array([1.,0.4,0.7,0.3], dtype = np.float32)

        """ send color to shader """
        glUniform4fv(Shaders.setColor_loc, 1, color)
            
        """ send matrix to shader """
        glUniformMatrix4fv(Shaders.model_loc, 1, GL_FALSE, entity.muscles[i].modelMatrix)

        """ draw vbo """
        glDrawElements(Graphics.styleIndex[vboId][vboDraw], Graphics.nbIndex[vboId][vboDraw], GL_UNSIGNED_INT, None)

        
def drawMuscleEdge(entity, style):
        
    if style != Graphics.opaque and style != Graphics.blending:
        return

    for i in range(0,len(entity.muscles)):

        """ verify matrix validity """
        if entity.muscles[i].modelMatrix == []:
            continue


        """ choose vbo """
        vboId = Graphics.vboHexagon
        vboDraw = Graphics.vboEdges
        """ bind surfaces vbo """
        Graphics.indexPositions[vboId][vboDraw].bind()
        Graphics.vertexPositions[vboId].bind()
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        """ choose color """
        if style == Graphics.opaque:
            color = np.array([0.5,0.5,0.5,1.], dtype = np.float32)
        elif style == Graphics.blending:
            if i+ID.offsetId(ID.MUSCLE) == SelectedMuscId:
                color = np.array([0.5,0.,0.,0.3], dtype = np.float32)
            elif i+ID.offsetId(ID.MUSCLE) == OverMuscId:
                color = np.array([1.,0.,0.,0.3], dtype = np.float32)
            else:
                color = np.array([0.5,0.7,0.7,0.3], dtype = np.float32)

        """ send color to shader """
        glUniform4fv(Shaders.setColor_loc, 1, color)
        
        """ send matrix to shader """
        glUniformMatrix4fv(Shaders.model_loc, 1, GL_FALSE, entity.muscles[i].modelMatrix)
            
        """ draw vbo """
        glDrawElements(Graphics.styleIndex[vboId][vboDraw], Graphics.nbIndex[vboId][vboDraw], GL_UNSIGNED_INT, None)