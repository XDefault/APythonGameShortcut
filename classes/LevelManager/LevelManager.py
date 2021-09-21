
class __LevelManager:

    __levels = []
    __CurrentLevel = None
    __CurrentLevelIndex = -9999
    __render = None

    def AddLevelToList(self,level):
        self.__levels.append(level)
    
    def LoadLevel(self,LevelIndex):
        print("   '->Loading: " + self.__levels[LevelIndex].name)
       
        #if(self.__CurrentLevel != None):                    #<--May be remove
        #    self.UnloadLevel(self.__CurrentLevelIndex)

        self.__levels[LevelIndex].SetRenderManager(self.__render)
        self.__InitLevelComponents(LevelIndex)

        self.__CurrentLevel = self.__levels[LevelIndex]
        self.__CurrentLevelIndex = LevelIndex

    def LoadLevelWithIndex(self,searchIndex):
        index = 0
        print("   '->Searching Level with internal index: " + str(searchIndex))
        for l in self.__levels:
            print("      '->Level Index " + str(l.index) + ": Checked")
            if(l.index == searchIndex):
                self.LoadLevel(index)
                return

            index += 1

        print("      '->No Level with Index "+ str(searchIndex)+" was Found")

    def LoadLevelWithName(self,searchName=str):
        index = 0
        print("   '->Searching Level with Name: " + searchName)
        for l in self.__levels:
            print("      '->Level Name - " + str(l.name) + ": Checked")
            if(l.name == searchName):
                self.LoadLevel(index)
                return

            index += 1

        print("      '->No Level with Name "+ searchName +" was Found")

    def UnloadLevel(self,LevelIndex):
        print("   '->Unload Level: " + self.__levels[LevelIndex].name)
        raise NotImplementedError
    
    def __InitLevelComponents(self,LevelIndex):
        print("      '->Init Level: " + self.__levels[LevelIndex].name)
        self.__levels[LevelIndex].InitObjects()
        #raise NotImplementedError

    def ArrangeLevelOrder(self):
        print("\nLevelManager")
        print("   '->Levels Rearranged")
        self.__levels.sort(key=lambda  n: n.GetIndex())
        print("   '->Current Level Order: " + str([str(e.index.__str__()+":"+e.name) for e in self.__levels]))

    def UpdateLevelEntities(self):
        self.__CurrentLevel.UpdateEntities()

    def SetRenderManager(self,render):
        self.__render = render

__manager = __LevelManager()


def GetStaticManager():
    global __manager
    if(__manager == None):
        try:
            __manager = __LevelManager()
        except:
            raise TypeError
    return __manager