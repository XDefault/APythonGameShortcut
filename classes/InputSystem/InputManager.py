import pygame
from classes.Events.EventTypes.InputEvent import InputEvent
from classes.Events import EventHandler
from classes.InputSystem.InputClass import Input
from classes.InputSystem.Keys import Key
from Configs import InputKeyMap as Map
from classes.Events import EventHandler
import keyboard

class __InputManagerHandler:
    __keysPressed = []
    __observers = []
    __enableAllKeys = False
    __EventHandler = EventHandler.GetStaticHandler()
    __Map = Map.GetStaticMap()

    def AddKeyPressToList(self,key=None):
        if(key != None):
            self.__keysPressed.append(key)      #Added to the list so its get executed

    def ExecuteKeysPressed(self):
        for k in self.__keysPressed:
            e = InputEvent(k)                               #Create a Event of Input
            self.__EventHandler.AddEventToSigleCheck(e)     #Send the Event to the Handler
            self.NotifyObservers(k)
        
        self.__keysPressed.clear()        #Clears the list for the next frame
    
    def GetKeyEvents(self):
        return self.__keysPressed         #Returns the list of keys on the frame for outside uses

    def on_pressed(self,key):
        
        keyPressed = None

        if(self.__enableAllKeys):
            keyPressed = Input(key.name) #Enable all the keys to be register e process by the manager
        
        for s in self.__Map.keys:      #Check keys on the list to see if the user input need it to be map to another key
            if(s.Input == key.name):
                keyPressed = Input(s.actionName)  #Remap the user input

        self.AddKeyPressToList(keyPressed) #Add To a list of keys to be notify to the observers

    def subscribeObserver(self,observer):   #Register functions to be notify without going though the EventManager
        if(self.__observers.__contains__(observer) == False):
            self.__observers.append(observer)
            print("\nInputManager")
            print("   '->Observer Subcribed: " + str(observer))

    def NotifyObservers(self,command):  #Notify any funcion subcribed as a observer and pass the key that was pressed
        for o in self.__observers:
            o(command)

__manager = __InputManagerHandler()         #Static InputManager so never happens to exists more than one

def GetStaticManager():
    global __manager
    if(__manager == None):
        try:
            __manager = __InputManagerHandler()
        except Exception as e:
            raise TypeError from e
    return __manager

def On_Pressed(key):
    #print(key.name)
    __manager.on_pressed(key)             #Send the key pressed to the InputManager

keyboard.on_press(callback=On_Pressed,suppress=True)    #Listen the keyboard for a key press