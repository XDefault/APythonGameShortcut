import pygame
from classes.EntityClasses.Entities import Entity

class __Render:

    to_render = []
    allLayers = []
    __current_camera = None
    render = pygame.sprite.Group()

    def draw_layers(self,display):
        self.__reorder_to_priority()
        for s in self.to_render:
            #print(self.GetLayerPriority(s))
            self.render.add(s.sprites)

        self.__update_pos_relative_to_camera()
        self.render.draw(display)
        self.render.empty()

    def get_layer_priority(self, layer_list):
        return layer_list.orderOfLayer

    def __reorder_to_priority(self):
        self.allLayers.sort(key=self.get_layer_priority)
        self.to_render = self.allLayers

    def add_layer_to_render(self,layer):
        layer.orderOfLayer = self.__check_for_correct_order_number(layer)
        self.allLayers.append(layer)

    def __check_for_correct_order_number(self,layer_to_convert):
        if not isinstance(layer_to_convert,BackgroundLayer):    #If its a normal layer and its set to a negative number its converted to the same positive number
            if layer_to_convert.order_of_layer < 0:
                return layer_to_convert.order_of_layer * -1

            return layer_to_convert.order_of_layer      #No Change was needed it

        if layer_to_convert.order_of_layer == 0:       #Any Background in layer 0, get in layer -1 to avoid conflict with the normal layers
            return -1
        if layer_to_convert.order_of_layer > 0:        #If its above 0 then its get convert to the same negative number
            return layer_to_convert.order_of_layer * -1

        return layer_to_convert.order_of_layer          #No change was needed it

    def get_index_of_layer_with_name(self,search_name:str):
        index = 0
        for l in self.allLayers:
            if l.layer_name == search_name:
                return index

            index += 1

        print("   '->No Layer with Name '" + search_name + "' Was Found")

    def set_current_camera(self,camera):
        self.__current_camera = camera

    def __update_pos_relative_to_camera(self):
        self.__current_camera.update()

        move_to = self.__current_camera.get_moveto()
        _x=move_to[0]
        _y=move_to[1]

        if(_x != 0 or _y != 0):
            for layer in self.to_render:
                for sprite in layer.sprites:
                    sprite.rect.centerx = sprite.rect.centerx - _x
                    sprite.rect.centery = sprite.rect.centery - _y

            self.__current_camera.set_moveto([0,0])

class Layer:

    def __init__(self):
        self.layer_name = ""
        self.sprites = []
        self.order_of_layer = 0

    def add_to_layer(self,sprite_to_render=Entity):
        self.sprites.append(sprite_to_render)

    def check_layer_for_entity(self,sprite=Entity):
        if self.sprites.__contains__(sprite):
            return True
        else:
            return False

    def remove_from_layer(self,entity=Entity):
        if self.check_layer_for_entity(entity) is True:
            self.sprites.remove(entity)


class BackgroundLayer(Layer):
    pass

__MANAGER = __Render()

def get_static_manager():
    global __MANAGER
    if __MANAGER is None:
        try:
            __MANAGER = __Render()
        except Exception as e:
            raise TypeError from e
    return __MANAGER
