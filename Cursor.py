import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

import Definitions
import Events
import Graphics
import GUI
import ID
import Limbs
import Muscles
import Sensors
import State
import StickMan

mouse = [0,0]
parent = -1
overID = 0
name = ''
info = []
def mouseManage():
    global overID
    global parent
    global name
    global info
    

    color = glReadPixels( mouse[0] , GUI.display[1] - mouse[1] - 1 , 1 , 1 , GL_RGBA , GL_FLOAT )
    r,g,b,a = 255*color[0][0]
    r = int(r)
    g = int(g)
    b = int(b)
    a = int(a)
    overID = ID.color2id(r,g,b)
    name = ''
    info = []

    parent = -1
    if ID.idCategory(overID) == ID.LIMB:
        parent = 0
    elif ID.idCategory(overID) == ID.MUSCLE:
        parent = 3
    elif ID.idCategory(overID) == ID.SENSOR or ID.idCategory(overID) == ID.ZOI:
        parent = 1
    elif ID.idCategory(overID) != 0:
        parent = 2
        
    if Events.setLookAt == True:
        if parent == -1:
            Limbs.lookingAtID = 0
        elif parent == 0:
            Limbs.lookingAtID = overID
    # select part
    GUI.overGuiId = 0
    Limbs.overLimbId = 0
    Sensors.overSensId = 0
    Muscles.OverMuscId = 0

    if parent == 0:
        Limbs.overLimbId = overID
        if Events.mouse_click == True:
            # place sensor on body
            if GUI.selectedTemplate != "":
                for sensorData in Sensors.sensorGraphics:
                    if GUI.selectedTemplate == sensorData.type:
                        r,g,b,a = sensorData.color
                        color = (r/255., g/255., b/255.)
                        Sensors.virtuSens = Sensors.virtuSens + [Sensors.sensors(StickMan.virtuMan.limbs[overID - ID.offsetId(ID.LIMB)].tag, sensorData.type, (0.,90,90), color)]
            # select limb
            else:
                Select = True
                for part in StickMan.selectedLimbs:
                    if part == StickMan.virtuMan.limbs[overID-1].tag:
                        Select = False
                        StickMan.selectedLimbs.remove(part)
                        break
                if Select == True:
                    StickMan.selectedLimbs += [StickMan.virtuMan.limbs[overID - ID.offsetId(ID.LIMB)].tag,]

        name = ' (' + StickMan.virtuMan.limbs[overID-1].tag + ')'
    elif parent == 1:
        Sensors.overSensId = overID
        if Events.mouse_click == True:
            if Sensors.selectedSens == overID:
                Sensors.selectedSens = 0
            else:
                Sensors.selectedSens = overID

            
        for indices in Definitions.packageIndices[2]:
            pack = Definitions.packagePreprocess[indices[0]][indices[1]]
            if pack[Definitions.packID] == Sensors.overSensId:
                
                if Events.mouse_click == True:
                    if GUI.selectedTemplate != "":
                        for sensorData in Sensors.sensorGraphics:
                            if GUI.selectedTemplate == sensorData.type:
                                r,g,b,a = sensorData.color
                                color = (r/255., g/255., b/255.)
                                Sensors.virtuSens = Sensors.virtuSens + [Sensors.sensors(pack[Definitions.entity].attach, sensorData.type, (pack[Definitions.entity].x,pack[Definitions.entity].t,pack[Definitions.entity].s), color)]
                        
                                Sensors.virtuSens[len(Sensors.virtuSens)-1].tag = pack[Definitions.entity].tag

                if Events.deleteSens == True:
                    if ID.idCategory(pack[Definitions.entity].id) == ID.SENSOR:
                        del Sensors.virtuSens[pack[Definitions.entity].id - ID.offsetId(ID.SENSOR)]

                name = ' (' + pack[Definitions.entity].type + ')'
                info = [str(pack[Definitions.entity].x) + ' ' + str(pack[Definitions.entity].t) + ' ' + str(pack[Definitions.entity].s), str(pack[Definitions.entity].id), str(pack[Definitions.entity].tag)]
                break
        
    if parent == 2:
        GUI.overGuiId = overID

        # windows
        if ID.idCategory(GUI.overGuiId) == ID.PANNEL:
            if Events.mouse_click == True:
                if GUI.selectedWindow != overID - ID.offsetId(ID.PANNEL):
                    GUI.selectedWindow = overID - ID.offsetId(ID.PANNEL)
                else:
                    GUI.selectedWindow = 0
               
        # groupes
        if ID.idCategory(GUI.overGuiId) == ID.GROUPE:
            if Events.mouse_click == True:
                State.sensorFileName[GUI.overGuiId-1 - ID.offsetId(ID.GROUPE)][1] = not State.sensorFileName[GUI.overGuiId-1 - ID.offsetId(ID.GROUPE)][1]
                State.loadGroups()
                if GUI.selectedGroup != overID:
                    GUI.selectedGroup = overID
                else:
                    GUI.selectedGroup = 0
            elif Events.setLookAt == True:
                Events.rename = State.sensorFileName[GUI.overGuiId-1 - ID.offsetId(ID.GROUPE)][0]
                Events.renameType = ID.GROUPE

        # templates
        if ID.idCategory(GUI.overGuiId) == ID.TEMPLATE:
            if Events.mouse_click == True:
                if GUI.selectedTemplate != Sensors.sensorGraphics[overID-1 - ID.offsetId(ID.TEMPLATE)].type:
                    GUI.selectedTemplate = Sensors.sensorGraphics[overID-1 - ID.offsetId(ID.TEMPLATE)].type
                else:
                    GUI.selectedTemplate = ""
                GUI.selectedZoi = ""
                State.loadZOI(GUI.selectedZoi)
            elif Events.setLookAt == True:
                Events.rename = Sensors.sensorGraphics[GUI.overGuiId-1 - ID.offsetId(ID.TEMPLATE)].type
                Events.renameType = ID.TEMPLATE

        # zoi
        if ID.idCategory(GUI.overGuiId) == ID.ZOILIST:
            if Events.mouse_click == True:
                if GUI.selectedZoi != State.zoiFileName[overID-1 - ID.offsetId(ID.ZOILIST)]:
                    GUI.selectedZoi = State.zoiFileName[overID-1 - ID.offsetId(ID.ZOILIST)]
                else:
                    GUI.selectedZoi = ""
                State.loadZOI(GUI.selectedZoi)
            elif Events.setLookAt == True:
                Events.rename = GUI.selectedZoi
                Events.renameType = ID.ZOILIST
        
        # postures
        if ID.idCategory(GUI.overGuiId) == ID.POSTURE:
            if Events.mouse_click == True:
                if GUI.selectedPosture != overID - ID.offsetId(ID.POSTURE):
                    GUI.selectedPosture = overID - ID.offsetId(ID.POSTURE)
                    State.loadPosture(StickMan.virtuMan)
                else:
                    GUI.selectedPosture = 0
            elif Events.setLookAt == True:
                Events.rename = State.postureFileName[GUI.overGuiId-1 - ID.offsetId(ID.POSTURE)]
                Events.renameType = ID.POSTURE

    if parent == 3:
        Muscles.OverMuscId = overID
        name = ' (' + StickMan.virtuMan.muscles[overID - ID.offsetId(ID.MUSCLE)].tag + ')'
        if Events.mouse_click == True:
            # place sensor on body
            if GUI.selectedTemplate != "":
                for sensorData in Sensors.sensorGraphics:
                    if GUI.selectedTemplate == sensorData.type:
                        r,g,b,a = sensorData.color
                        color = (r/255., g/255., b/255.)
                        Sensors.virtuSens = Sensors.virtuSens + [Sensors.sensors(StickMan.virtuMan.muscles[Muscles.OverMuscId - ID.offsetId(ID.MUSCLE)].tag, sensorData.type, (0.,90,90), color)]
            # select limb
            else:
                if Muscles.SelectedMuscId != overID:
                    Muscles.SelectedMuscId = overID
                else:
                    Muscles.SelectedMuscId = 0
    else:
        pass