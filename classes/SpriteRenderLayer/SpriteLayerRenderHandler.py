import pygame
from classes.EntityClasses.Entities import Entity

class __Render:

    toRender = []
    allLayers = []
    __currentCamera = None

    def DrawLayers(self,Display):
        render = pygame.sprite.Group()
        self.ReorderToPriority()
        for s in self.toRender:
            #print(self.GetLayerPriority(s))
            render.add(s.sprites)

        self.__UpdatePosRelativeToCamera()    
        render.draw(Display)
        render.empty()
    
    def GetLayerPriority(self, layerList):
        return layerList.orderOfLayer

    def ReorderToPriority(self):
        self.allLayers.sort(key=self.GetLayerPriority)
        self.toRender = self.allLayers

    def AddLayerToRender(self,layer):
        layer.orderOfLayer = self.__CheckForCorrectOrderNumber(layer)
        self.allLayers.append(layer)

    def __CheckForCorrectOrderNumber(self,layerToConvert):
        if(isinstance(layerToConvert,BackgroundLayer) == False):    #If its a normal layer and its set to a negative number its converted to the same positive number
            if(layerToConvert.orderOfLayer < 0):
                return layerToConvert.orderOfLayer * -1
            
            return layerToConvert.orderOfLayer      #No Change was needed it
        
        if(layerToConvert.orderOfLayer == 0):       #Any Background in layer 0, get in layer -1 to avoid conflict with the normal layers
            return -1
        if(layerToConvert.orderOfLayer > 0):        #If its above 0 then its get convert to the same negative number
            return layerToConvert.orderOfLayer * -1
        
        return layerToConvert.orderOfLayer          #No change was needed it

    def GetIndexOfLayerWithName(self,searchName:str):
        index = 0
        for l in self.allLayers:
            if (l.layerName == searchName):
                return index
            
            index += 1

        print("   '->No Layer with Name '" + searchName + "' Was Found")

    def SetCurrentCamera(self,camera):
        self.__currentCamera = camera

    def __UpdatePosRelativeToCamera(self):
        self.__currentCamera.update()

        moveTo = self.__currentCamera.GetMoveTo()
        x=moveTo[0]
        y=moveTo[1]

        if(x != 0 or y != 0):
            for l in self.toRender:
                for s in l.sprites:
                    s.rect.centerx = s.rect.centerx - x
                    s.rect.centery = s.rect.centery - y

            self.__currentCamera.SetMoveTo([0,0])

class Layer:

    def __init__(self):
        self.layerName = ""
        self.sprites = []
        self.orderOfLayer = 0

    def AddToLayer(self,spriteToRender=Entity):
        self.sprites.append(spriteToRender)

    def CheckLayerForEntity(self,sprite=Entity):
        if(self.sprites.__contains__(sprite)):
            return True
        else:
            return False

    def RemoveFromLayer(self,entity=Entity):
        if(self.CheckLayerForEntity(entity) == True):
            self.sprites.remove(entity)


class BackgroundLayer(Layer):

    def AddToLayer(self,spriteToRender=Entity):
        self.sprites.append(spriteToRender)

__manager = __Render()

def GetStaticManager():
    global __manager
    if(__manager == None):
        try:
            __manager = __Render()
        except Exception as e:
            raise TypeError from e
    return __manager