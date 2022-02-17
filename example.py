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
Displaysurf = pygame.display.set_mode(Configuration.DISPLAYRES)
Displaysurf.fill((255,255,255))
pygame.display.set_caption("Game")

#Language Manager
LangManager.change_language(LangManager.Langs.EN)        #Set the Language to english
current_game_lang = LangManager.get_text_by_value("Lang")  #Get the text in json file based on the key value passed and language selected

#Set Entities And Groups

#Setting Entities can be done inside a level class------------------------------------------------------------
staticEntity = StaticEntity()       #Creating a Static Entity and not setting a ID so a random will be generated
staticEntity.set_id_name("Floor1")    #Setting a ID through a function
#staticEntity.use_gravity(False)     #Static entities by default are set to not be affected by gravity
staticEntity.spawn_point(150,500)    #Setting the SpawnPoint Position
staticEntity.scale_entity(300,100)

normalEntity = Entity("Floor2")     #Creating a Normal Entity and setting a ID right at the start
normalEntity.use_gravity(False)      #Setting to not be affected by gravity
normalEntity.spawn_point(350,400)    #Setting a SpawnPoint Position
normalEntity.static_physics(True)    #Setting so physics are not to be controlled by the Physics Engine, it will still stop other entities
#normalEntity.scale_entity(300,100)

Floor3 = StaticEntity("Floor3")     #Creating a Normal Entity and setting a ID right at the start
Floor3.spawn_point(150,200)    #Setting a SpawnPoint Position
#Floor3.scale_entity(300,100)

player1 = Player("Player1")  #Creating a player and setting a ID right at the start
player1.static_physics(False) #Setting the player physics to be controlled by the Physics Engine
player1.spawn_point(50,300)   #Setting the SpawnPoint Position
player1.use_gravity(True)     #Setting the player to be affected by gravity
player1.scale_entity(50,100)
#--------------------------------------------------------------------------------------------------------------

print("\nEntities Info")
print("   '->staticEntity ID: "+staticEntity.get_id_name())   #Printing the ID for the example above
print("   '->normalEntity ID: "+normalEntity.get_id_name())
print("   '->player1 ID: "+player1.get_id_name())             #Printing the ID for the example above

playerGroup = pygame.sprite.Group(staticEntity) #Setting up a group of sprites
playerGroup.add(player1)                        #Adding up the second player as part of the group
playerGroup.add(normalEntity)
playerGroup.add(Floor3)

#Set Physics Engine
PEngine = PhysicsManager(Displaysurf)           #Passing the Display of the game to the Physics Engine
PEngine.add_entity_to_physics(staticEntity)        #Setting the entities that should be affected by the Physics Engine
PEngine.add_entity_to_physics(player1)
PEngine.add_entity_to_physics(normalEntity)
PEngine.add_entity_to_physics(Floor3)

#Set Render
render = RenderManager.get_static_manager()

#Set Camera
camera = Camera()                               #Creating or setting up a camera can be done inside a level class
render.set_current_camera(camera)
camera.set_camera_pos([-30,20])

#Set Sprite Layers
layer1 = Layer()
layer1.order_of_layer = 0             #Normal Layers never stays a negative number, the system will make a positive number
layer1.layer_name = "Normal Layer"   #Setting a name so the level class can add entities to this layer

layer2 = BackgroundLayer()
layer2.order_of_layer = 1             #Background Layers will always become a negative number, if it is set to 0 the system will make be -1
layer2.layer_name = "Background Layer"

#Add entities to layers
layer1.add_to_layer(staticEntity)
layer2.add_to_layer(player1)
layer1.add_to_layer(normalEntity)
layer2.add_to_layer(Floor3)
#Set Layer To Render
render.add_layer_to_render(layer1)
render.add_layer_to_render(layer2)

#Set a static Input Manager and Event Handler
inputManager = InputManager.get_static_manager() #Using the manager inside the script so there never more than one
eventHandler = EventHandler.get_static_manager() #Using the event handler in the script so there never more than one
inputManager.subscribe_observer(player1.controlled_movement_example)#Setting the fuctions that should be notify
                                                                    #when the player hits a key on the keyboard

#Set a static Level Manager and loading a level
levelManager = LevelManager.get_static_manager()                #Using the manager inside the script so there never more than one
levelManager.set_render_manager(render)                         #Passing the render manager so level class can add entities to a layer to be render
levelManager.add_level_to_list(ExampleLevelClass())             #Adding the level to the manager list and passing the render
levelManager.arrange_level_order()                              #Arranging the order of the levels based on their internal index variable
#levelManager.load_level(0)                                     #Load the first item on the level list
#levelManager.load_level_with_index(1)                          #Load level with the internal index of 1
levelManager.load_level_with_name(search_name="Example Level")  #Load level with the name "Example Level"
                                                                #IMPORTANT ----> Loading any level will already unload the previous one by default
#levelManager.unload_level(0)                                   #Stop rendering any entity previously loaded by the first level on the list
#levelManager.unload_level_with_index(1)                        #Stop rendering any entity previously loaded by the level with the internal index of 1
levelManager.unload_level_with_name(search_name="Example Level")#Stop rendering any entity previously loaded by the level with the name "Example Level"

myText = pygame.font.SysFont('Comic Sans MS',30)

#Game Loop
def game_loop():
    while True:
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        inputManager.execute_keys_pressed()  #Execute key strokes
        eventHandler.events_single_check()   #Execute events and remove then from the list

        PEngine.update()                   #Update the physics every frame

        Displaysurf.fill(COLORS.GRAY)

        playerGroup.update()
        levelManager.update_level_entities() #Update entities on current loaded level

        render.draw_layers(Displaysurf)     #Render the layers to the display

        #Setting up the text to use the translation from the json file
        textSurface = myText.render("Current Language: "+current_game_lang,False,(0,0,0))

        #Draw the text to the screen
        Displaysurf.blit(textSurface,(0,0))

        #Show the rect of entities
        pygame.draw.rect(Displaysurf,COLORS.RED,player1.rect,1)
        pygame.draw.rect(Displaysurf,COLORS.BLUE,staticEntity.rect,1)
        pygame.draw.rect(Displaysurf,COLORS.GREEN,normalEntity.rect,1)
        pygame.draw.rect(Displaysurf,COLORS.CYAN,Floor3.rect,1)

        pygame.display.update()
        FramePerSec.tick(Configuration.FPS)

def main():
    game_loop()

if __name__ == "__main__":
    main()
    