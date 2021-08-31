import sys
import pygame
from Configs.ConfigurationHandler import Configuration
from Configs.ColorsConfig import COLORS
from classes.Enemys.enemyBasicModule import Enemy
from classes.SpriteRenderLayer.SpriteLayerRenderHandler import *
from classes.InputSystem import InputManager
from classes.Events import EventHandler
from classes.PhysicsEngine.PhysicsSystem import PhysicsManager
from classes.LanguageSystem import LanguageManager as LangManager

#Setup Game
pygame.init()

FramePerSec = pygame.time.Clock()
Displaysurf = pygame.display.set_mode(Configuration.DisplayRes)
Displaysurf.fill((255,255,255))
pygame.display.set_caption("Game")

#Language Manager
LangManager.ChangeLanguage(LangManager.Langs.EN)        #Set the Language to english
currentGameLang = LangManager.GetTextByValue("Lang")    #Get the text in json file based on the key value passed and language selected

#Set Entities And Groups
enemy = Enemy()             #Creating a Enemy and not setting a ID so a random will be generated
enemy.SetIDName("Enemy1")   #Setting a ID through a function
enemy.UseGravity(False)     #Setting the enemy to not be affected by gravity
enemy.SpawnPoint(50,500)    #Setting the SpawnPoint Position
     
player = Enemy("Player")    #Creating a "Enemy" and setting a ID right at the start
player.StaticPhysics(False) #Setting the player physics to be controlled by the Physics Engine
player.SpawnPoint(50,300)   #Setting the SpawnPoint Position
player.UseGravity(True)     #Setting the enemy to not be affected by gravity

print("enemy ID: "+enemy.GetIDName())   #Printing the ID for the example above
print("player ID: "+player.GetIDName()) #Printing the ID for the example above

enemyGroup = pygame.sprite.Group(enemy) #Setting up a group of sprites
enemyGroup.add(player)                  #Adding up the player as part of the group

#Set Physics Engine
PEngine = PhysicsManager(Displaysurf)   #Passing the Display of the game to the Physics Engine
PEngine.AddEntityToPhysics(enemy)       #Setting the entities that should be affected by the Physics Engine
PEngine.AddEntityToPhysics(player)

#Set Render
render = Render()

#Set Sprite Layers
layer1 = Layer()
layer1.orderOfLayer = 0

layer2 = BackgroundLayer()
layer2.orderOfLayer = 1

#Add entities to layers
layer1.AddToLayer(enemy)
layer2.AddToLayer(player)

#Set Layer To Render
render.AddLayerToRender(layer1)
render.AddLayerToRender(layer2)

#Set a static Input Manager and Event Handler
inputManager = InputManager.manager            #Using the manager inside the script so there never more than one
eventHandler = EventHandler.GetStaticHandler() #Using the event handler in the script so there never more than one
inputManager.subscribeObserver(player.ControlledMovementExample)    #Setting the fuctions that should be notify  
                                                                    #when the player hits a key on the keyboard

myText = pygame.font.SysFont('Comic Sans MS',30)

#Game Loop
while True:  
    for event in  pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
    
    inputManager.ExecuteKeysPressed()  #Execute key strokes
    eventHandler.EventsSingleCheck()   #Execute events and remove then from the list
    
    PEngine.Update()                   #Update the physics every frame

    Displaysurf.fill(COLORS.GRAY)
    
    enemyGroup.update()

    render.DrawLayers(Displaysurf)     #Render the layers to the display

    #Setting up the text to use the translation from the json file
    textSurface = myText.render("Current Language: "+currentGameLang,False,(0,0,0))
    
    #Draw the text to the screen
    Displaysurf.blit(textSurface,(0,0))
    
    pygame.display.update()

    FramePerSec.tick(Configuration.FPS)