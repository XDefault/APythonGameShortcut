from classes.EntityClasses.Entities import AnimatedEntity
from classes.EntityClasses.Animator import Animation
from Configs.ConfigurationHandler import Configuration
from Configs import InputKeyMap

class Enemy(AnimatedEntity):
    
    spritesheetPath = "images/Sheet.jpg"
    rectsPos = []
   
    #animations = [[(3,0,24,29),(30,0,24,29),(58,0,24,29),(87,0,24,29),(115,0,24,29),(143,0,24,29),(171,0,24,29),(199,0,24,29)],
    #                [(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29)]]
    
    animations = [Animation("idle",[(3,0,24,29),(30,0,24,29),(58,0,24,29),(87,0,24,29),(115,0,24,29),(143,0,24,29),(171,0,24,29),(199,0,24,29)]),
                    Animation("test",[(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29)])]

    animationNames = ["idle","test"]
    
    
    Speed = 10
    movingTo = 1 #0 = left | 1 = right
    TravelDist = 500

    ObjWidth = 100
    ObjHeight = 150
    def __init__(self,ID=None):
        super(Enemy,self).__init__(ID)

    def move(self):
        if(self.rect.right <=self.InitX or self.rect.right >= self.InitX + self.TravelDist):
            self.Speed *= -1

        self.rect.move_ip(self.Speed,0)

    def ControlledMovementExample(self,keydown):
        #print(InputKeyMap.staticInputMap.GetKey("up"))
        #print(keydown.key + " | " +  InputKeyMap.staticInputMap.GetKeyByActionName("up") + " | " +  InputKeyMap.staticInputMap.GetActionNameByKey("w"))
        if(keydown.key == "up"):
            self.moveByPhysics(0,-1)
        elif(keydown.key == "down"):
            self.moveByPhysics(0,1)
        elif(keydown.key == "left"):
            self.moveByPhysics(-1,0)
        elif(keydown.key == "right"):
            self.moveByPhysics(1,0)