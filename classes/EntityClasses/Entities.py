import pygame
import random
from classes.SpriteSheetHandler.SpriteSheetHandler import SpriteSheet
from Configs.PhysicsConfig import Gravity,PhysicsUpdateRate,DisInsideCollisionToDetect
from Configs.ConfigurationHandler import Configuration

class Entity(pygame.sprite.Sprite):

    __UsedID = []

    def __init__(self,IDName=None):
        super().__init__()
        #private variables
        self.__IDName = "Entity"
        self.__StaticPhysics: bool = False
        self.__UseGravity:bool = True
        self.__velocity:float = [0,0]
        self.__collidingWith:pygame.sprite = []
        self.__isGrounded:bool = False

        #public variables
        self.Rot_Angle = 0
        self.Sprite = "images/InitSprite.jpg"
        self.initImage = pygame.image.load(self.Sprite)
        self.image = self.initImage
        self.LoadedSprite = self.image
        self.surf = pygame.Surface((32,32))
        self.InitX = 30
        self.InitY = 100
        self.ObjWidth = 50
        self.ObjHeight = 100
        self.rect = self.surf.get_rect(center = (self.InitX,self.InitY))
        self.Scale(self.ObjWidth,self.ObjHeight)
        self.CurrentPosX = 30
        self.CurrentPosY = 100

        if(IDName == None):                             #Set a random ID if none
            data = range(1,15000)
            newId = random.sample(data,1)

            if(self.__UsedID.__contains__(newId)):
                newId = random.sample(data,1)
            else:
                self.__UsedID.append(newId)
                self.SetIDName(str(random.sample(data,1)))
        else:
            self.SetIDName(IDName)
        
    def UpdateLoadedSprite(self,sprite):
        self.LoadedSprite = sprite

    def draw(self,surface):                             #Draw entity on screen
        surface.blit(self.image,self.rect)

    def SetStaticSprite(self,newImagePath):
        self.image = pygame.image.load(newImagePath)

    def SpawnPoint(self,newX,newY):                     #Set initial spawn coords
        self.InitX = newX
        self.InitY = newY
        self.rect = self.surf.get_rect(center = (self.InitX,self.InitY))

#Normal Entity Alterations------------------------------------------------------------------------------------
    def move(self,xAmount,yAmount):                     #Move the entity without the physics
        self.rect.move_ip(xAmount,yAmount)

    def Scale(self,x,y):                                #Scale the entity
        self.ObjWidth = x
        self.ObjHeight = y

        self.image = pygame.transform.scale(self.image,(self.ObjWidth,self.ObjHeight))
        self.rect = self.image.get_rect(center=self.rect.center)

    def Rot_Center(self,angle):                         #Rotate the entity with the center as a pivot point
        self.Rot_Angle += angle
        
        self.image = pygame.transform.rotate(self.LoadedSprite, self.Rot_Angle)

    def isGrounded(self):
        return self.__isGrounded
#Physics Related----------------------------------------------------------------------------------------------

    def UpdateEntityPhysics(self):                      #Update the physics of this entity
        self.__isGrounded = False
        if(self.__StaticPhysics == False):
            self.rect.move_ip(self.__velocity[0],self.__velocity[1])
            
            self.__DeAcceleratePhysic(3)

            if(self.__UseGravity == True and self.__isGrounded == False):
                self.__velocity[1] += Gravity
            
        self.__CheckCollisions()
        self.__collidingWith.clear()

    def HasCollisionWith(self,sprite:pygame.sprite):    #Return a bool if the entity has collision with the other entity
       
        if(self.rect.colliderect(sprite.rect)): #if(self.rect.colliderect(sprite.rect)):
            if(self.__IDName == sprite.GetIDName()):
                #print("Its the same " + self.__IDName)
                return False
            #print(self.GetIDName() + " | " + sprite.GetIDName())
            return True
        else:
            return False

    def AddCollisionToList(self,sprite:pygame.sprite):  #Add a collision to the list to be processed
        if not self.__collidingWith.__contains__(sprite):
            self.__collidingWith.append(sprite)

    def __CheckCollisions(self):
        currentX = self.__velocity[0]
        currentY = self.__velocity[1]
        #print(self.__IDName+" collidingWith len: " + str(len(self.__collidingWith)))
        for c in self.__collidingWith:
            if(self.rect.colliderect(c.rect)):
                
                colDir = self.__GetCollisionDir(c)

                if(colDir == "top"):
                    if(self.__StaticPhysics == False):
                        if(self.__CheckDistanceInsideCollision(c,colDir) > 0):
                            self.rect.move_ip(0,1)
                    if(self.__velocity[1] < 0):
                        currentY = 0
                        
                elif(colDir == "left"):
                    if(self.__StaticPhysics == False):
                        if(self.__CheckDistanceInsideCollision(c,colDir) > 0):
                            self.rect.move_ip(1,0)
                    if(self.__velocity[0] > 0):
                        currentX = 0
                        
                elif(colDir == "right"):
                    if(self.__StaticPhysics == False):
                        if(self.__CheckDistanceInsideCollision(c,colDir) > 0):
                            self.rect.move_ip(-1,0)
                    if(self.__velocity[0]<0):
                        currentX = 0

                elif(colDir == "bottom"):
                    if(self.__StaticPhysics == False):
                        if(self.__CheckDistanceInsideCollision(c,colDir) > DisInsideCollisionToDetect):
                            self.rect.move_ip(0,-1)
                        self.__isGrounded = True
                    if(self.__velocity[1] > 0):
                        currentY = 0
                
                #if(self.__IDName == "Player1" or self.__IDName == "Player2"):
                #    print(self.__IDName + " has collision from " + colDir)

        self.SetVelocity(currentX,currentY)
    
    def __CheckDistanceInsideCollision(self,sprite,Dir):
        if(Dir == "top"):
            return self.rect.top - sprite.rect.bottom
        elif(Dir == "left"):
            return self.rect.left - sprite.rect.right
        elif(Dir == "bottom"):
            return self.rect.bottom - sprite.rect.top
        else:
            return self.rect.right - sprite.rect.left

    def __GetCollisionDir(self,sprite:pygame.sprite):
        dr = abs(self.rect.right - sprite.rect.left)
        dl = abs(self.rect.left - sprite.rect.right)
        db = abs(self.rect.bottom - sprite.rect.top)
        dt = abs(self.rect.top - sprite.rect.bottom)

        if(min(dl,dr) < min(dt,db)):
            direction = "left" if dl < dr else "right"
        else:
            direction = "bottom" if db < dt else "top"
        
        return direction

    def __DeAcceleratePhysic(self,ratio):

        velocityAmount = (PhysicsUpdateRate*Configuration.FPS)/(Configuration.FPS / 2.5)
        #print(velocityAmount)
        
        if(self.__velocity[0] > 0.1):                   #Horizontal Axis
            self.__velocity[0] -= ratio * velocityAmount # velocity = velocity - (massRatio * ((updateRate * FPS) / (FPS / 2.5)))
        elif(self.__velocity[0] < -0.1):
            self.__velocity[0] += ratio * velocityAmount
        else:
            self.__velocity[0] = 0.0
            
        if(self.__velocity[1] > 0.1):                  #Vertical Axis
            self.__velocity[1] -= ratio * velocityAmount
        elif(self.__velocity[1] < -0.1):
            self.__velocity[1] += ratio * velocityAmount
        else:
            self.__velocity[1] = 0.0
       
        #print("DeAccreleratePhysic")

    def moveByPhysics(self,xAmount,yAmount):            #Add a force to push the entity in a direction
        if(self.__StaticPhysics == False):
            self.__velocity[0] += (xAmount*10) * PhysicsUpdateRate
            self.__velocity[1] += (yAmount*10) * PhysicsUpdateRate
            #self.rect.move_ip(self.velocity[0],self.velocity[1])

    def GetVelocity(self):
        return self.__velocity

    def GetVelocityX(self):
        return self.__velocity[0]

    def GetVelocityY(self):
        return self.__velocity[1]

    def SetVelocity(self,X,Y):
        self.__velocity[0] = X
        self.__velocity[1] = Y

    def UseGravity(self,switch:bool):
        self.__UseGravity = switch

    def StaticPhysics(self,switch:bool):                #Change the physics to be controlled by something else
        self.__StaticPhysics = switch

    def GetStaticPhysics(self):
        return self.__StaticPhysics
#ID Related---------------------------------------------------------------------------------------------------

    def GetIDName(self):
        return self.__IDName 

    def SetIDName(self,newID):
        self.__IDName = newID

class AnimatedEntity(Entity):

    spritesheetPath = ""
    #---Animation Related Variables-------------------------------------------------------------------
    rectsPos = []                                       #Current sprites rect to get from spriteSheet
    images = []
    transparancyColor = None
    currentAnimation = ""                               #Ease check for wich animations is been played
    animations = []                                   #All Animations that can be played by this Entity
    
    #--------------------------------------------------------------------------------------------------

    def __init__(self,IDName=None):
        super(AnimatedEntity,self).__init__(IDName)
        self.ss = SpriteSheet(self.spritesheetPath)
        
        
        self.index = 0
        self.SetAnimation("idle")
        self.image = self.images[self.index]
        self.rect = self.surf.get_rect(center = (self.InitX,self.InitY))
    
    def update(self):                                   #Update the image on the entity
        self.index += 1

        if(self.index >= len(self.images)):
            self.index = 0
        
        self.UpdateLoadedSprite(self.images[self.index])
        #self.image = self.LoadedSprite
        self.Rot_Center(0)                              #This already update the self.image
        self.Scale(self.ObjWidth,self.ObjHeight)

    def SetAnimation(self,animationName=None):          #Change animation to the name specify
        animationSelect = 0
        #print(self.animations[0].animationName)

        for animation in self.animations:
            if(animation.animationName == animationName):
                print("\nAnimatedEntity")
                print("   '->Entity ID: "+self.GetIDName())
                print("   '->Animation Before: "+self.currentAnimation+" | Rect Before" + str(self.rectsPos))
                self.currentAnimation = animation.animationName
                self.rectsPos = self.animations[animationSelect].animation
                self.images = self.ss.images_at(self.rectsPos,self.transparancyColor)
                print("   '->Animation After: "+self.currentAnimation+' | Rect After' + str(self.rectsPos))
                self.index = 0
                return
            
            animationSelect += 1
                
        
        print("No Animation was Found")

    def testAnimation(self,key):
        if(key != ""):
            self.SetAnimation("test")

class StaticEntity(Entity):

    def __init__(self,IDName=None):
        super(StaticEntity,self).__init__(IDName)
        super(StaticEntity,self).UseGravity(False)
        super(StaticEntity,self).StaticPhysics(True)