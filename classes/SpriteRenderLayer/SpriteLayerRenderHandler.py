import pygame
from classes.EntityClasses.Entities import Entity

class __Render:

    toRender = []
    allLayers = []

    def DrawLayers(self,Display):
        render = pygame.sprite.Group()
        self.ReorderToPriority()
        for s in self.toRender:
            #print(self.GetLayerPriority(s))
            render.add(s.sprites)
            

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

class Layer:
    layerName = ""
    sprites = []
    orderOfLayer = 0

    def AddToLayer(self,spriteToRender=Entity):
        self.sprites.append(spriteToRender)


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