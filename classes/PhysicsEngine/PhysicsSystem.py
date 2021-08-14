import pygame
from Configs.PhysicsConfig import PhysicsUpdateRate
from Configs.ConfigurationHandler import Configuration

class PhysicsManager:
    
    __ToUpdate = []
    __allEntitys:pygame.sprite = []
    __Timer = 0.0
    __display = pygame.rect
    __PhysicsDisplayRatio = 2 #Extra size outside the screen that physics still should affect (1 = disable this function)

    def __init__(self,SurfaceDisplay:pygame.Surface):
        self.__SetDisplay(SurfaceDisplay)

    def __CheckEntitysToUpdate(self): #Check if entities are inside the of the range to be updated

        for s in self.__allEntitys:
            if(self.__display.colliderect(s.rect)):
                self.__ToUpdate.append(s)       #Add the entity that is inside the range to a list

        self.__UpdateCalculationPhysics()       #Not implemented

        self.__Timer = 0.0                      #Reset the timer

    def __SetDisplay(self,display:pygame.Surface):  #Set the size of the rectangle that only entities that are inside will update 
                                                    #their physics, this is based on the current size of the display
        self.__display = display.get_rect()
        self.__display.w = self.__display.w * self.__PhysicsDisplayRatio
        self.__display.h = self.__display.h * self.__PhysicsDisplayRatio
        self.__display.x -= self.__display.w * (self.__PhysicsDisplayRatio/6)
        self.__display.y -= self.__display.h * (self.__PhysicsDisplayRatio/6)
        print("Display (w,h,x,y): "+str(self.__display.w) + "," + str(self.__display.h) + "," + str(self.__display.x) + "," + str(self.__display.y))
        
    def AddEntityToPhysics(self,entity):    #Add the entity to a list so i can be manage by the system and updated when it need
        if(self.__allEntitys.__contains__(entity) ==  False):
            self.__allEntitys.append(entity)

    def __UpdatePhysics(self):       
        if(self.__Timer >= PhysicsUpdateRate):  #Update the entities check at a regular interval set in the config file
            self.__CheckEntitysToUpdate()

    def __CheckCollisions(self):      #Check for collisions between the entities in a list

        for s in self.__ToUpdate:     #Check every entity againts any other in the list to see if its has any collision

            for c in self.__ToUpdate:
                if(s.HasCollisionWith(c)):   
                    s.AddCollisionToList(c) #Adds any collision that happens into a list
                
            s.UpdateEntityPhysics()         #Update each entity physics

        self.__ToUpdate.clear()             #Clear the list for next frame

    def __UpdateCalculationPhysics(self):
        try:
            raise NotImplementedError       #Will always pass
        except:
            pass

    def Update(self):
        self.__Timer += 1/(Configuration.FPS)
        self.__UpdatePhysics()
        self.__CheckCollisions()
