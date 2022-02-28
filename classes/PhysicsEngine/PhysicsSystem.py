import pygame
from Configs.PhysicsConfig import PHYSICS_UPDATE_RATE,DIS_INSIDE_COLLISION,GRAVITY
from Configs.ConfigurationHandler import Configuration

class PhysicsManager:

    __to_update = []
    __all_entitys:pygame.sprite = []
    __timer = 0.0
    __display = pygame.rect
    __physics_display_ratio = 2 #Extra size outside the screen that physics still should affect (1 = disable this function)
    __FRAMES_TO_WAIT_BOUNCE = 3 #Wait for frames after a bounce to set entity._is_grounded = true

    def __init__(self,SurfaceDisplay:pygame.Surface):
        self.__set_display(SurfaceDisplay)

    def __check_entitys_to_update(self): #Check if entities are inside the of the range to be updated

        for s in self.__all_entitys:
            if self.__display.colliderect(s.rect):
                self.__to_update.append(s)       #Add the entity that is inside the range to a list

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

    def clamp(self,number,minimum_value,maximum_value):
        return max(minimum_value, min(number, maximum_value))

    def __bounce(self,h:float,bounce_amount:float):
        #print(math.sin(self.clamp(t,0,1) * math.pi) * bounce_amount)
        #return math.sin(self.clamp(t,0,1) * math.pi) * bounce_amount
        return (h * 0.6) * bounce_amount

    def __has_collision_with(self,sprite1:pygame.sprite,sprite2:pygame.sprite):    #Return a bool if the entity has collision with the other entity

        if sprite1.rect.colliderect(sprite2.rect): #if(self.rect.colliderect(sprite.rect)):
            if sprite1.get_id_name() == sprite2.get_id_name():
                #print("Its the same " + self.__id_name)
                return False
            #print(self.get_id_name() + " | " + sprite.get_id_name())
            return True
        else:
            return False

    def __get_collision_dir(self,sprite1:pygame.sprite,sprite2:pygame.sprite):
        dr = abs(sprite1.rect.right - sprite2.rect.left)
        dl = abs(sprite1.rect.left - sprite2.rect.right)
        db = abs(sprite1.rect.bottom - sprite2.rect.top)
        dt = abs(sprite1.rect.top - sprite2.rect.bottom)

        if min(dl,dr) < min(dt,db):
            direction = "left" if dl < dr else "right"
        else:
            direction = "bottom" if db < dt else "top"

        return direction

    def __get_distance_inside_collision(self,sprite1,sprite2,direction):
        if direction == "top":
            return sprite1.rect.top - sprite2.rect.bottom
        elif direction == "left":
            return sprite1.rect.left - sprite2.rect.right
        elif direction == "bottom":
            return sprite1.rect.bottom - sprite2.rect.top
        else:
            return sprite1.rect.right - sprite2.rect.left

    def __apply_gravity(self,sprite,amount):
        if sprite.get_use_gravity():
            sprite.set_velocity_y(sprite.get_velocity_y() + amount)

    def __check_entity_collisions(self,sprite1:pygame.sprite,sprite2:pygame.sprite):
        current_x = sprite1.get_velocity_x()
        current_y = sprite1.get_velocity_y()
        #print(sprite1.__id_name+" collidingWith len: " + str(len(sprite1.__colliding_with)))

        if sprite1.rect.colliderect(sprite2.rect):

            col_dir = self.__get_collision_dir(sprite1,sprite2)
            insidedis = self.__get_distance_inside_collision(sprite1,sprite2,col_dir)

            if col_dir == "top":
                if not sprite1.get_static_physics():
                    if insidedis > DIS_INSIDE_COLLISION:
                        sprite1.rect.move_ip(0,insidedis)
                if sprite1.get_velocity_y() < 0:
                    current_y = 0

            elif col_dir == "left":
                if not sprite1.get_static_physics():
                    if insidedis > DIS_INSIDE_COLLISION:
                        sprite1.rect.move_ip(insidedis,0)
                if sprite1.get_velocity_x() < 0:
                    current_x = 0

            elif col_dir == "right":
                if not sprite1.get_static_physics():
                    if insidedis > DIS_INSIDE_COLLISION:
                        sprite1.rect.move_ip(-insidedis,0)
                if sprite1.get_velocity_x() >0:
                    current_x = 0

            elif col_dir == "bottom":
                sprite1._set_is_grounded(True)
                if not sprite1.get_static_physics():

                    #print(sprite1.get_id_name() + " insidedis: " + str(insidedis))
                    if insidedis > DIS_INSIDE_COLLISION:
                        sprite1.rect.move_ip(0,-insidedis)
                
                    #current_y = 0
                    
                    if sprite1.get_velocity_y() > 1:
                        current_y = 0

                    current_y = self.bounce_update_y(sprite1,sprite2)
            #if(sprite1.__id_name == "Player1" or sprite1.__id_name == "Player2"):
            #    print(sprite1.__id_name + " has collision from " + col_dir)
        sprite1.set_velocity(current_x,current_y)

    def bounce_update_y(self,sprite,col):   #TODO bounce in all directions
        #print(sprite.get_velocity_y())
        if sprite.get_velocity_y() < 6:
            return 0

        velocity_y = sprite.get_velocity_y()
        velocity_y = self.__bounce(velocity_y,(sprite.get_bounce() + col.get_bounce()) / 2)
        return -velocity_y

    def __deaccelerate_entity_physic(self,entity,ratio):

        velocity_amount = (PHYSICS_UPDATE_RATE*Configuration.FPS)/(Configuration.FPS / 2.5)
        #print(velocity_amount)

        if entity.get_velocity_x() > 0.1:                   #Horizontal Axis
            entity.set_velocity_x(entity.get_velocity_x() - (ratio * velocity_amount)) # velocity = velocity - (massRatio * ((updateRate * FPS) / (FPS / 2.5)))
        elif entity.get_velocity_x() < -0.1:
            entity.set_velocity_x(entity.get_velocity_x() + (ratio * velocity_amount))
        else:
            entity.set_velocity_x(0.0)

        if entity.get_velocity_y() > 0.1:                   #Vertical Axis
            entity.set_velocity_y(entity.get_velocity_y() - (ratio * velocity_amount))
        elif entity.get_velocity_y() < -0.1:
            entity.set_velocity_y(entity.get_velocity_y() + (ratio * velocity_amount))
        else:
            entity.set_velocity_y(0.0)

    def __check_collisions(self,sprite1):      #Check for collisions between the entities in a list

        if sprite1.get_static_physics():
            return

        for sprite2 in self.__to_update:
            if self.__has_collision_with(sprite1,sprite2):
                self.__check_entity_collisions(sprite1,sprite2)

    def update_entity_physics(self,sprite):                      #Update the physics of this entity
        sprite.rect.move_ip(sprite.get_velocity_x(),sprite.get_velocity_y())

    def __update_physics(self):
        if self.__timer >= PHYSICS_UPDATE_RATE:  #Update the entities check at a regular interval set in the config file
            self.__check_entitys_to_update()

            for entity in self.__to_update:
                if entity.get_use_gravity:
                    self.__apply_gravity(entity,GRAVITY)

                self.__deaccelerate_entity_physic(entity,3)

                if entity.get_velocity_y() < -3:    #Delay some frames to give the player time to jump again when bouncing
                    if entity._wait_frames_after_bounce > self.__FRAMES_TO_WAIT_BOUNCE:
                        entity._set_is_grounded(False)
                        entity._wait_frames_after_bounce = 0
                    else:
                        entity._wait_frames_after_bounce += 1

                self.update_entity_physics(entity)         #Update each entity physics
                self.__check_collisions(entity)

            self.__to_update.clear()             #Clear the list for next frame

    def update(self):
        self.__timer += 1/(Configuration.FPS)
        self.__update_physics()
