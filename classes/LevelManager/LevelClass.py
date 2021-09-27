from classes.EntityClasses.Entities import Entity

class Level:

    __RenderManager = None

    def __init__(self):
        self.name = "name"
        self.__index = 0
        self.levelEntities = []
        

    def AddEntityToLevel(self,item=Entity,onNameLayer=str):
        if(self.levelEntities.__contains__(item) == False):
            self.levelEntities.append(item)
            self.__RenderManager.allLayers[self.__RenderManager.GetIndexOfLayerWithName(onNameLayer)].AddToLayer(item)

    def InitObjects(self):
        print("         '->InitObj: " + self.name)
        #pass

    def GetIndex(self):
        return self.__index

    def UpdateEntities(self):
        #print("         '->UpdateEntities: " + self.name)
        for o in self.levelEntities:
            o.update()

    def SetRenderManager(self,render):
        self.__RenderManager = render