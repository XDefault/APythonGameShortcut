from classes.EntityClasses.Entities import AnimatedEntity
from classes.EntityClasses.Animator import Animation

class Player(AnimatedEntity):

    spritesheetPath = 'images\\InitSprite.jpg'

    animations = [Animation("idle",[(3,0,24,29),(30,0,24,29),(58,0,24,29),(87,0,24,29),(115,0,24,29),(143,0,24,29),(171,0,24,29),(199,0,24,29)]),
                    Animation("test",[(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29),(6,0,24,29)])]

    speed = 10

    def __init__(self,ID=None):
        super(Player,self).__init__(ID)
        self.ObjWidth = 50

    def auto_move_to_the_sides(self):
        if(self.rect.right <=self.InitX or self.rect.right >= self.InitX + self.TravelDist):
            self.speed *= -1

        self.rect.move_ip(self.speed,0)

    def controlled_movement_example(self,keydown):
        if(keydown.key == "up" and self.is_grounded()):
            self.move_by_physics(0,-100)
        elif keydown.key == "down":
            self.move_by_physics(0,1)
        elif keydown.key == "left":
            self.move_by_physics(-3,0)
        elif keydown.key == "right":
            self.move_by_physics(3,0)
