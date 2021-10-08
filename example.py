import sys
import pygame
from Configs.ConfigurationHandler import Configuration
from Configs.ColorsConfig import COLORS
from classes.Player.PlayerExampleModule import Player
from classes.EntityClasses.Entities import StaticEntity,Entity
from classes.SpriteRenderLayer import SpriteLayerRenderHandler as RenderManager
from classes.SpriteRenderLayer.SpriteLayerRenderHandler import Layer,BackgroundLayer
from classes.InputSystem import InputManager
from classes.Events import EventHandler
from classes.PhysicsEngine.PhysicsSystem import PhysicsManager
from classes.LanguageSystem import LanguageManager as LangManager
from classes.LevelManager import LevelManager
from classes.LevelManager.Levels.ExampleLevel import ExampleLevelClass
from classes.Camera.CameraClass import Camera

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

#Setting Entities can be done inside a level class------------------------------------------------------------
staticEntity = StaticEntity()       #Creating a Static Entity and not setting a ID so a random will be generated
staticEntity.SetIDName("Floor1")    #Setting a ID through a function
#staticEntity.UseGravity(False)     #Static entities by default are set to not be affected by gravity
staticEntity.SpawnPoint(150,500)    #Setting the SpawnPoint Position
staticEntity.Scale(300,100)         

normalEntity = Entity("Floor2")     #Creating a Normal Entity and setting a ID right at the start
normalEntity.UseGravity(False)      #Setting to not be affected by gravity
normalEntity.SpawnPoint(350,400)    #Setting a SpawnPoint Position
normalEntity.StaticPhysics(True)    #Setting so physics are not to be controlled by the Physics Engine, it will still stop other entities
#normalEntity.Scale(300,100)

player1 = Player("Player1")  #Creating a player and setting a ID right at the start
player1.StaticPhysics(False) #Setting the player physics to be controlled by the Physics Engine
player1.SpawnPoint(50,300)   #Setting the SpawnPoint Position
player1.UseGravity(True)     #Setting the player to be affected by gravity
#--------------------------------------------------------------------------------------------------------------

print("\nEntities Info")
print("   '->staticEntity ID: "+staticEntity.GetIDName())   #Printing the ID for the example above
print("   '->normalEntity ID: "+normalEntity.GetIDName())
print("   '->player1 ID: "+player1.GetIDName())             #Printing the ID for the example above

playerGroup = pygame.sprite.Group(staticEntity) #Setting up a group of sprites
playerGroup.add(player1)                        #Adding up the second player as part of the group
playerGroup.add(normalEntity)

#Set Physics Engine
PEngine = PhysicsManager(Displaysurf)           #Passing the Display of the game to the Physics Engine
PEngine.AddEntityToPhysics(staticEntity)        #Setting the entities that should be affected by the Physics Engine
PEngine.AddEntityToPhysics(player1)
PEngine.AddEntityToPhysics(normalEntity)

#Set Render
render = RenderManager.GetStaticManager()

#Set Camera
camera = Camera()                               #Creating or setting up a camera can be done inside a level class
render.SetCurrentCamera(camera)
camera.SetCameraPos([-30,20])

#Set Sprite Layers
layer1 = Layer()
layer1.orderOfLayer = 0             #Normal Layers never stays a negative number, the system will make a positive number
layer1.layerName = "Normal Layer"   #Setting a name so the level class can add entities to this layer

layer2 = BackgroundLayer()
layer2.orderOfLayer = 1             #Background Layers will always become a negative number, if it is set to 0 the system will make be -1
layer2.layerName = "Background Layer"

#Add entities to layers
layer1.AddToLayer(staticEntity)
layer2.AddToLayer(player1)
layer1.AddToLayer(normalEntity)
#Set Layer To Render
render.AddLayerToRender(layer1)
render.AddLayerToRender(layer2)

#Set a static Input Manager and Event Handler
inputManager = InputManager.GetStaticManager() #Using the manager inside the script so there never more than one
eventHandler = EventHandler.GetStaticHandler() #Using the event handler in the script so there never more than one
inputManager.subscribeObserver(player1.ControlledMovementExample)   #Setting the fuctions that should be notify  
                                                                    #when the player hits a key on the keyboard

#Set a static Level Manager and loading a level
levelManager = LevelManager.GetStaticManager()              #Using the manager inside the script so there never more than one
levelManager.SetRenderManager(render)                       #Passing the render manager so level class can add entities to a layer to be render
levelManager.AddLevelToList(ExampleLevelClass())            #Adding the level to the manager list and passing the render   
levelManager.ArrangeLevelOrder()                            #Arranging the order of the levels based on their internal index variable
#levelManager.LoadLevel(0)                                  #Load the first item on the level list
#levelManager.LoadLevelWithIndex(1)                         #Load level with the internal index of 1
levelManager.LoadLevelWithName(searchName="Example Level")  #Load level with the name "Example Level"
                                                            #IMPORTANT ----> Loading any level will already unload the previous one by default
#levelManager.UnloadLevel(0)                                #Stop rendering any entity previously loaded by the first level on the list
#levelManager.UnloadLevelWithIndex(1)                       #Stop rendering any entity previously loaded by the level with the internal index of 1
levelManager.UnloadLevelWithName(searchName="Example Level")#Stop rendering any entity previously loaded by the level with the name "Example Level"

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
    
    playerGroup.update()
    levelManager.UpdateLevelEntities() #Update entities on current loaded level

    render.DrawLayers(Displaysurf)     #Render the layers to the display

    #Setting up the text to use the translation from the json file
    textSurface = myText.render("Current Language: "+currentGameLang,False,(0,0,0))
    
    #Draw the text to the screen
    Displaysurf.blit(textSurface,(0,0))
    
    #Show the rect of entities
    pygame.draw.rect(Displaysurf,COLORS.RED,player1.rect,1)
    pygame.draw.rect(Displaysurf,COLORS.BLUE,staticEntity.rect,1)
    pygame.draw.rect(Displaysurf,COLORS.GREEN,normalEntity.rect,1)
    
    pygame.display.update()
    FramePerSec.tick(Configuration.FPS)