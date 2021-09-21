from classes.EntityClasses.Entities import Entity

class Level:

    RenderManager = ""

    def __init__(self):
        self.name = "name"
        self.__index = 0
        self.levelEntities = []
        

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

    def SetRenderManager(self,render):
        self.RenderManager = render