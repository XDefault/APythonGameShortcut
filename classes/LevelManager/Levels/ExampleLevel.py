from classes.LevelManager.LevelClass import Level
from classes.EntityClasses.Entities import staticEntity

class ExampleLevelClass(Level):

    exampleGroup = ""


    def __init__(self,render=None):
        super(ExampleLevelClass,self).__init__(render)
        self.name = "Example Level"
        self.index = 1

    def InitObjects(self):
        super().InitObjects()                   #This is just to debug, it can be ignore
        entity = staticEntity("static_obj")
        entity.SpawnPoint(30,100)

        self.RenderManager.allLayers[0].AddToLayer(entity)

        self.AddEntityToLevel(entity)
