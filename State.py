import os

import StickMan

path = "States/"
fileName = []
currentFile = 0

def createList():
    global fileName
    print(" - creating list of models - ")
    fileName = os.listdir(path)
    print(fileName)

callSave = False
def save(entity):
    global callSave
    print("save model : {}".format(fileName[currentFile]))

    file = open(path + fileName[currentFile], 'w')

    for part in entity.parts:
        file.write(part[StickMan.Data_id])
        file.write("\n")
        wat = " ".join(str(e) for e in part[StickMan.Data_angle])
        file.write(wat)
        file.write("\n")
    file.close()
    callSave = False
    
    
callLoad = False
def load(entity):
    global callLoad
    print("load model : {}".format(fileName[currentFile]))

    file = open(path + fileName[currentFile], 'r')

    for part in entity.parts:
        line = file.readline() # read part name
        line = file.readline() # read part orientations
        values = map(float, line.split())
        part[StickMan.Data_angle] = values
    file.close()
    callLoad = False