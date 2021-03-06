from classes.LevelManager.LevelClass import Level
from classes.EntityClasses.Entities import StaticEntity

class ExampleLevelClass(Level):

    exampleGroup = ""

    def __init__(self):
        super().__init__()
        self.name = "Example Level"
        self.index = 1

    def init_objects(self):
        super().init_objects()                   #This is just to debug, it can be ignore

        entity = StaticEntity("static_obj")
        entity.spawn_point(30,100)

        self.add_entity_to_level(entity,on_name_layer="Normal Layer")    #Add Entity to the level and adds to a render layer
