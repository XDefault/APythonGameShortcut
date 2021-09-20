from classes.EntityClasses.Entities import Entity

class Level:

    def __init__(self):
        self.name = "name"
        self.__index = 0
        self.levelObjects = []

    def AddObjectToLevel(self,item=Entity):
        self.levelObjects.append(item)

    def InitObjects(self):
        print("         '->InitObj: " + self.name)
        pass

    def GetIndex(self):
        return self.__index