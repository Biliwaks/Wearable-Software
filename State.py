import os

import Events
import Graphics
import GUI
import StickMan
import Sensors

pathModels = "States/Models/"
pathGroups = "States/Groups/"
pathTemplates = "States/Templates/"
pathUserSettings = "States/UserSettings/"
pathZoi = "States/Zoi/"
extension = ".txt"
currentModelFile = 0
modelFileName = []
currentSensorFile = 0
saveGroupFile = "Default" + extension
sensorFileName = []

def importUserSettings():
    file = open(pathUserSettings + "Resolution.txt", 'r')
    line = file.readline()
    x, y = line.split(' ')
    GUI.display[0] = int(x)
    GUI.display[1] = int(y)

def renameFile(key):
    if Events.renameType == GUI.guiTemplate:
        if key == 'backspace' and len(Events.rename) >= 5:
            os.rename(pathTemplates + Events.rename, pathTemplates + Events.rename[:-5] + extension)
            os.rename(pathZoi + Events.rename, pathZoi + Events.rename[:-5] + extension)
            Events.rename = Events.rename[:-5] + extension
        elif key == 'space':
            key = ' '
        if Events.caps == True:
            key = key.upper()
        if len(key) == 1:
            os.rename(pathTemplates + Events.rename, pathTemplates + Events.rename[:-4] + key + extension)
            os.rename(pathZoi + Events.rename, pathZoi + Events.rename[:-4] + key + extension)
            Events.rename = Events.rename[:-4] + key + extension

    elif Events.renameType == GUI.guiGroup:
        if key == 'backspace' and len(Events.rename) >= 5:
            os.rename(pathGroups + Events.rename, pathGroups + Events.rename[:-5] + extension)
            Events.rename = Events.rename[:-5] + extension
        elif key == 'space':
            key = ' '
        if Events.caps == True:
            key = key.upper()
        if len(key) == 1:
            os.rename(pathGroups + Events.rename, pathGroups + Events.rename[:-4] + key + extension)
            Events.rename = Events.rename[:-4] + key + extension

def createList():
    global modelFileName
    global sensorFileName

    modelFileName = os.listdir(pathModels)

    listFiles = os.listdir(pathGroups)
    sensorFileName = []
    for file in listFiles:
        sensorFileName = sensorFileName + [[file, False]]
    
    zoiFileName = os.listdir(pathZoi)
    
def updateTemplateList():
    global sensorFileName
    listFiles = os.listdir(pathGroups)
    tempList = []
    for file in listFiles:
        tempList = tempList + [[file, False]]
    for fileName in sensorFileName:
        for i in range(0,len(tempList)):
            if fileName[0] == tempList[i][0]:
                tempList[i][1] = fileName[1]
    sensorFileName = tempList

    templateFileName = os.listdir(pathTemplates)
    Sensors.sensorGraphics = []
    for template in templateFileName:
        file = open(pathTemplates + template, 'r')
        line = file.readline()
        if line == "":
            continue
        r, g, b, a, shape = line.split(' ')
        Sensors.sensorGraphics = Sensors.sensorGraphics + [[template[:-len(extension)], (int(r),int(g),int(b),int(a)), int(shape)]]
        file.close()

"""
    Human model files
"""
def saveModel(entity):
    print("save model : {}".format(modelFileName[currentModelFile]))

    file = open(pathModels + modelFileName[currentModelFile], 'w')

    for part in entity.parts:
        file.write(part[StickMan.Data_id])
        file.write("\n")
        angle = " ".join(str(e) for e in part[StickMan.Data_angle])
        file.write(angle)
        file.write("\n")
        swing = " ".join(str(e) for e in part[StickMan.Data_swing])
        file.write(swing)
        file.write("\n")
        twist = " ".join(str(e) for e in part[StickMan.Data_twist])
        file.write(twist)
        file.write("\n")
    file.close()

    
def loadModel(entity):
    print("load model : {}".format(modelFileName[currentModelFile]))

    file = open(pathModels + modelFileName[currentModelFile], 'r')

    while True:
        ID = file.readline() # read part name
        if ID == "":
            break
        ID = ID[:-1] # remove end of line character
        line = file.readline() # read part orientations
        angle = map(float, line.split())
        line = file.readline() # read part orientations
        swing = map(float, line.split())
        line = file.readline() # read part orientations
        twist = map(float, line.split())
        for part in entity.parts:
            #print(part[StickMan.Data_id])
            if part[StickMan.Data_id] == ID:
                part[StickMan.Data_angle] = angle
                part[StickMan.Data_swing] = swing
                part[StickMan.Data_twist] = twist
                break
    file.close()

"""
    Template files
"""
def saveTemplates(template):
    file = open(pathTemplates + template[0] + extension, 'w')

    file.write(str(template[1][0]))
    file.write(" ")
    file.write(str(template[1][1]))
    file.write(" ")
    file.write(str(template[1][2]))
    file.write(" ")
    file.write(str(template[1][3]))
    file.write(" ")
    file.write(str(template[2]))

    file.close()

"""
    Sensors files
"""
def saveSensors():
    print("save sensor group : {}".format(saveGroupFile))

    file = open(pathGroups + saveGroupFile, 'w')

    for sensor in Sensors.virtuSens:
        file.write(sensor.attach)
        file.write(" ")
        file.write(sensor.type)
        file.write(" ")
        file.write(str(sensor.x))
        file.write(" ")
        file.write(str(sensor.t))
        file.write(" ")
        file.write(str(sensor.s))
        file.write("\n")
    file.close()

def loadSensors():
    Sensors.virtuSens = []

    for file in sensorFileName:
        if file[1] == True:
            print("load sensor group : {}".format(file[0]))

            file = open(pathGroups + file[0], 'r')
    
            while True:
                line = file.readline() # read sensor data
                if line == "":
                    break
                parent, type, x, t, s = line.split(' ')
                Sensors.virtuSens = Sensors.virtuSens + [Sensors.sensors(parent, type, (float(x),float(t),float(s)))]
            file.close()


"""
    Zones of interest files
"""
#def saveZoi(sensor):
#    print("save sensor group : {}".format(sensorFileName[currentSensorFile][0]))
#
#    file = open(pathZoi + sensor.type + extension, 'w')
#    
#    file.write(str(sensor.color[0]))
#    file.write(" ")
#    file.write(str(sensor.color[1]))
#    file.write(" ")
#    file.write(str(sensor.color[2]))
#    file.write(" 255 ")
#    file.write(sensor.type) #string here, int when read. fix it.
#    file.close()

def loadZOI(zoiFileName):
    Sensors.zoiSens = []

    if zoiFileName[0] == "":
        return

    print("load zoi : {}".format(zoiFileName[0]))

    file = open(pathZoi + zoiFileName[0] + '.txt', 'r')
    
    color = (0.5,0.5,0.5,1)
    type = zoiFileName[0]
    while True:
        line = file.readline() # read sensor data
        if line == "":
            break
        parent, x, t, s = line.split(' ')
        Sensors.zoiSens = Sensors.zoiSens + [Sensors.sensors(parent, type, (float(x),float(t),float(s)), color)]
        Sensors.zoiSens[len(Sensors.zoiSens)-1].tag = 'Zoi'
    file.close()