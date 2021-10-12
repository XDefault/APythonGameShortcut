from classes.EntityClasses.Entities import Entity

class Level:

    __render_manager = None

    def __init__(self):
        self.name = "name"
        self.__index = 0
        self.level_entities = []


    def add_entity_to_level(self,item=Entity,on_name_layer=str):
        if not self.level_entities.__contains__(item):
            self.level_entities.append(item)
            self.__render_manager.allLayers[self.__render_manager.get_index_of_layer_with_name(on_name_layer)].add_to_layer(item)

    def init_objects(self):
        print("         '->InitObj: " + self.name)
        #pass

    def get_index(self):
        return self.__index

    def update_entities(self):
        #print("         '->UpdateEntities: " + self.name)
        for o in self.level_entities:
            o.update()

    def set_render_manager(self,render):
        self.__render_manager = render

    def unload_entities_on_level(self):
        for e in self.level_entities:
            for l in self.__render_manager.allLayers:
                l.remove_from_layer(e)
