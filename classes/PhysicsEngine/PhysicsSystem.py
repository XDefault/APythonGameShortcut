import pygame
from Configs.PhysicsConfig import PHYSICS_UPDATE_RATE
from Configs.ConfigurationHandler import Configuration

class PhysicsManager:

    __to_update = []
    __all_entitys:pygame.sprite = []
    __timer = 0.0
    __display = pygame.rect
    __physics_display_ratio = 2 #Extra size outside the screen that physics still should affect (1 = disable this function)

    def __init__(self,SurfaceDisplay:pygame.Surface):
        self.__set_display(SurfaceDisplay)

    def __check_entitys_to_update(self): #Check if entities are inside the of the range to be updated

        for s in self.__all_entitys:
            if self.__display.colliderect(s.rect):
                self.__to_update.append(s)       #Add the entity that is inside the range to a list

        #self.__update_calculation_physics()       #Not implemented

        self.__timer = 0.0                      #Reset the timer

    def __set_display(self,display:pygame.Surface): #Set the size of the rectangle that only entities that are inside will update
                                                    #their physics, this is based on the current size of the display
        self.__display = display.get_rect()
        self.__display.w = self.__display.w * self.__physics_display_ratio
        self.__display.h = self.__display.h * self.__physics_display_ratio
        self.__display.x -= self.__display.w * (self.__physics_display_ratio/6)
        self.__display.y -= self.__display.h * (self.__physics_display_ratio/6)
        print("\nPhysicsEngine")
        display = display.get_rect()
        print("   '->Display (w,h,x,y): " + str(display.w) + "," + str(display.h) + "," + str(display.x) + "," + str(display.y))
        print("   '->Active Physics Zone (w,h,x,y): "+str(self.__display.w) + "," + str(self.__display.h) + "," + str(self.__display.x) + "," + str(self.__display.y))

    def add_entity_to_physics(self,entity):    #Add the entity to a list so i can be manage by the system and updated when it need
        if not self.__all_entitys.__contains__(entity):
            self.__all_entitys.append(entity)

    def __update_physics(self):
        if self.__timer >= PHYSICS_UPDATE_RATE:  #Update the entities check at a regular interval set in the config file
            self.__check_entitys_to_update()

    def __check_collisions(self):      #Check for collisions between the entities in a list

        for s in self.__to_update:     #Check every entity againts any other in the list to see if its has any collision
            if s.get_static_physics():
                continue
            for c in self.__to_update:
                if s.has_collision_with(c):
                    s.add_collision_to_list(c) #Adds any collision that happens into a list

                s.update_entity_physics()         #Update each entity physics

        self.__to_update.clear()             #Clear the list for next frame

    def __update_calculation_physics(self):
        try:
            raise NotImplementedError
        except Exception as e:
            raise ValueError from e

    def update(self):
        self.__timer += 1/(Configuration.FPS)
        self.__update_physics()
        self.__check_collisions()
