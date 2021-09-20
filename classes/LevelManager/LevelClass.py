from classes.EntityClasses.Entities import Entity

class Level:

    def __init__(self,render):
        self.name = "name"
        self.__index = 0
        self.levelEntities = []
        self.RenderManager = render

    def AddEntityToLevel(self,item=Entity):
        self.levelEntities.append(item)

    def InitObjects(self):
        print("         '->InitObj: " + self.name)
        pass

    def GetIndex(self):
        return self.__index

    def UpdateEntities(self):
        #print("         '->UpdateEntities: " + self.name)
        for o in self.levelEntities:
            o.update()