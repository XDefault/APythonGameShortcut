import random

class Camera:

    __usedIndex = []
    #TODO Animated Camera Pos

    def __init__(self,name=None):
        self.__index = self.__GenerateIndex()
        
        if(name == None):
            self.__name = "Camera " + str(self.__index)
        else:
            self.__name = name
   
        self.__Pos = [-6,0]
        self.__MoveTo = [0,0]

    def __GenerateIndex(self):
        data = range(1,15000)
        newId = random.sample(data,1)

        while(self.__usedIndex.__contains__(newId)):
            newId = random.sample(data,1)
            
        self.__usedIndex.append(newId)
        return newId

    def GetCameraName(self):
        return self.__name

    def GetCameraIndex(self):
        return self.__index

    def GetCameraPos(self):
        return self.__Pos

    def GetCameraPosX(self):
        return self.__Pos[0]

    def GetCameraPosY(self):
        return self.__Pos[1]

    def SetCameraPos(self,pos):
        self.__MoveTo[0] = pos[0] - self.__Pos[0]
        self.__MoveTo[1] = pos[1] - self.__Pos[1]
        self.__Pos = pos

    def SetCameraPosX(self,posx):
        self.__MoveTo[0] = posx - self.__Pos[0]
        self.__Pos[0] = posx

    def SetCameraPosY(self,posy):
        self.__MoveTo[1] = posy - self.__Pos[1]
        self.__Pos[1] = posy

    def GetMoveTo(self):        #This is meant to be used only by the render 
        return self.__MoveTo
    
    def SetMoveTo(self,pos):    #This is meant to be used only by the render 
        self.__MoveTo = pos

    def update(self):
        pass