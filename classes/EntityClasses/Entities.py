import random
import pygame
from classes.SpriteSheetHandler.SpriteSheetHandler import SpriteSheet
from Configs.PhysicsConfig import PHYSICS_UPDATE_RATE


class Entity(pygame.sprite.Sprite):

    __UsedID = []

    def __init__(self,id_name=None):
        super().__init__()
        #private variables
        self.__id_name = "Entity"
        self.__static_physics: bool = False
        self.__use_gravity:bool = True
        self.__velocity:float = [0,0]
        self.__is_grounded:bool = False

        #public variables
        self.rot_angle = 0
        self.sprite = "images/InitSprite.jpg"
        self.init_image = pygame.image.load(self.sprite)
        self.image = self.init_image
        self.loaded_sprite = self.image
        self.surf = pygame.Surface((32,32))
        self.init_x = 30
        self.init_y = 100
        self.obj_width = 100
        self.obj_height = 100
        #self.rect = self.surf.get_rect(center = (self.init_x,self.init_y))
        self.rect = self.loaded_sprite.get_rect(center=(self.init_x,self.init_y))
        self.scale_entity(self.obj_width,self.obj_height)

        if id_name is None:                             #Set a random ID if none
            data = range(1,15000)
            new_id = random.sample(data,1)

            while self.__UsedID.__contains__(new_id):
                new_id = random.sample(data,1)

            self.__UsedID.append(new_id)
            self.set_id_name(str(random.sample(data,1)))
        else:
            self.set_id_name(id_name)

    def update_loaded_sprite(self,sprite):
        self.loaded_sprite = sprite

    def update_rect(self):
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self,surface):                             #Draw entity on screen
        surface.blit(self.image,self.rect)

    def set_static_sprite(self,new_image_path):
        self.image = pygame.image.load(new_image_path)

    def spawn_point(self,new_x,new_y):                     #Set initial spawn coords
        self.init_x = new_x
        self.init_y = new_y
        self.rect = self.surf.get_rect(center = (self.init_x,self.init_y))

    def update(self):
        self.update_rect()

#Normal Entity Alterations------------------------------------------------------------------------------------
    def move(self,x_amount,y_amount):                     #Move the entity without the physics
        self.rect.move_ip(x_amount,y_amount)

    def scale_entity(self,x,y):                                #Scale the entity
        self.obj_width = x
        self.obj_height = y

        self.image = pygame.transform.scale(self.image,(self.obj_width,self.obj_height))
        self.update_loaded_sprite(self.image)
        #self.rect = self.image.get_rect(center=self.rect.center)

    def rot_center(self,angle):                         #Rotate the entity with the center as a pivot point
        self.rot_angle += angle

        self.image = pygame.transform.rotate(self.loaded_sprite, self.rot_angle)
        #self.rect = self.image.get_rect(center=self.rect.center)

    def is_grounded(self):
        return self.__is_grounded
#Physics Related----------------------------------------------------------------------------------------------

    def _set_is_grounded(self,value:bool):
        self.__is_grounded = value

    def move_by_physics(self,x_amount,y_amount):            #Add a force to push the entity in a direction
        if self.__static_physics:
            return

        if y_amount < 0:
            self._set_is_grounded(False)

        self.__velocity[0] += (x_amount*20) * PHYSICS_UPDATE_RATE
        self.__velocity[1] += (y_amount*20) * PHYSICS_UPDATE_RATE

    def get_velocity(self):
        return self.__velocity

    def get_velocity_x(self):
        return self.__velocity[0]

    def get_velocity_y(self):
        return self.__velocity[1]

    def set_velocity_x(self,value):
        self.__velocity[0] = value

    def set_velocity_y(self,value):
        self.__velocity[1] = value

    def set_velocity(self,X,Y):
        self.__velocity[0] = X
        self.__velocity[1] = Y

    def use_gravity(self,switch:bool):
        self.__use_gravity = switch

    def get_use_gravity(self):
        return self.__use_gravity

    def static_physics(self,switch:bool):                #Change the physics to be controlled by something else
        self.__static_physics = switch

    def get_static_physics(self):
        return self.__static_physics
#ID Related---------------------------------------------------------------------------------------------------

    def get_id_name(self):
        return self.__id_name

    def set_id_name(self,new_id):
        self.__id_name = new_id

class AnimatedEntity(Entity):

    #---Animation Related Variables-------------------------------------------------------------------
    spritesheetPath = ""
    rects_pos = []                                       #Current sprites rect to get from spriteSheet
    images = []
    transparancyColor = None
    current_animation = ""                               #Ease check for wich animations is been played
    animations = []                                   #All Animations that can be played by this Entity

    #--------------------------------------------------------------------------------------------------

    def __init__(self,IDName=None):
        super(AnimatedEntity,self).__init__(IDName)
        self.ss = SpriteSheet(self.spritesheetPath)


        self.index = 0
        self.set_animation("idle")
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(self.init_x,self.init_y))

    def update(self):                                   #Update the image on the entity
        self.index += 1

        if self.index >= len(self.images):
            self.index = 0

        self.__update_image_status()

    def __update_image_status(self):
        self.update_loaded_sprite(self.images[self.index])
        self.rot_center(0)
        self.scale_entity(self.obj_width,self.obj_height)
        self.update_rect()

    def set_animation(self,animation_name=None):          #Change animation to the name specify
        animation_select = 0
        #print(self.animations[0].animation_name)

        for animation in self.animations:
            if animation.animation_name == animation_name:
                print("\nAnimatedEntity")
                print("   '->Entity ID: "+self.get_id_name())
                print("   '->Animation Before: "+self.current_animation+" | Rect Before" + str(self.rects_pos))
                self.current_animation = animation.animation_name
                self.rects_pos = self.animations[animation_select].animation
                self.images = self.ss.images_at(self.rects_pos,self.transparancyColor)
                print("   '->Animation After: "+self.current_animation+' | Rect After' + str(self.rects_pos))
                self.index = 0
                return

            animation_select += 1


        print("No Animation was Found")


    def test_animation(self,key):
        if key != "":
            self.set_animation("test")

class StaticEntity(Entity):

    def __init__(self,id_name=None):
        super(StaticEntity,self).__init__(id_name)
        super(StaticEntity,self).use_gravity(False)
        super(StaticEntity,self).static_physics(True)
