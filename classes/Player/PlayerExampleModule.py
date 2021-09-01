from classes.EntityClasses.Entities import AnimatedEntity
from classes.EntityClasses.Animator import Animation
from Configs.ConfigurationHandler import Configuration
from Configs import InputKeyMap

class Player(AnimatedEntity):
    
    spritesheetPath = 'images\\InitSprite.jpg'
   
    animations = [Animation("idle",[(3,0,24,29),(30,0,24,29),(58,0,24,29),(87,0,24,29),(115,0,24,29),(143,0,24,29),(171,0,24,29),(199,0,24,29)]),
                    Animation("test",[(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29)])]
    
    Speed = 10
    #movingTo = 1 #0 = left | 1 = right

    ObjWidth = 100
    ObjHeight = 150

    def __init__(self,ID=None):
        super(Player,self).__init__(ID)

    def AutoMoveToTheSides(self):
        if(self.rect.right <=self.InitX or self.rect.right >= self.InitX + self.TravelDist):
            self.Speed *= -1

        self.rect.move_ip(self.Speed,0)

    def ControlledMovementExample(self,keydown):
        if(keydown.key == "up"):
            self.moveByPhysics(0,-1)
        elif(keydown.key == "down"):
            self.moveByPhysics(0,1)
        elif(keydown.key == "left"):
            self.moveByPhysics(-1,0)
        elif(keydown.key == "right"):
            self.moveByPhysics(1,0)