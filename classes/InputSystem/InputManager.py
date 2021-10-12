import keyboard
from classes.Events.EventTypes.InputEvent import InputEvent
from classes.Events import EventHandler
from classes.InputSystem.InputClass import Input
from Configs import InputKeyMap as Map

class __InputManagerHandler:
    __keys_pressed = []
    __observers = []
    __enableAllKeys = False
    __EventHandler = EventHandler.get_static_manager()
    __Map = Map.GetStaticMap()

    def add_key_press_to_list(self,key=None):
        if key is not None:
            for k in self.__keys_pressed:
                if k.key == key.key:
                    return

            self.__keys_pressed.append(key)      #Added to the list so its get executed

    def execute_keys_pressed(self):
        for k in self.__keys_pressed:
            e = InputEvent(k)                                   #Create a Event of Input
            self.__EventHandler.add_event_to_sigle_check(e)     #Send the Event to the Handler
            self.notify_observers(k)

        #self.__keys_pressed.clear()        #Clears the list for the next frame

    def get_key_events(self):
        return self.__keys_pressed          #Returns the list of keys on the frame for outside uses

    def on_pressed(self,key):

        key_pressed = None

        if self.__enableAllKeys:
            key_pressed = Input(key.name)   #Enable all the keys to be register e process by the manager

        for s in self.__Map.keys:           #Check keys on the list to see if the user input need it to be map to another key
            if s.key_input == key.name:
                key_pressed = Input(s.action_name)  #Remap the user input

        if key_pressed is not None:
            self.add_key_press_to_list(key_pressed) #Add To a list of keys to be notify to the observers

    def on_release(self,key):

        key_pressed = None

        if self.__enableAllKeys:
            key_pressed = Input(key.name)   #Enable all the keys to be register e process by the manager

        for s in self.__Map.keys:           #Check keys on the list to see if the user input need it to be map to another key
            if s.key_input == key.name:
                key_pressed = Input(s.action_name)

        if key_pressed is not None:
            self.remove_from_list(key_pressed.key)

    def remove_from_list(self,key):
        for k in self.__keys_pressed:
            if k.key == key:
                self.__keys_pressed.remove(k)

    def subscribe_observer(self,observer):   #Register functions to be notify without going though the EventManager
        if not self.__observers.__contains__(observer):
            self.__observers.append(observer)
            print("\nInputManager")
            print("   '->Observer Subcribed: " + str(observer))

    def notify_observers(self,command):  #Notify any funcion subcribed as a observer and pass the key that was pressed
        for o in self.__observers:
            o(command)

__MANAGER = __InputManagerHandler()         #Static InputManager so never happens to exists more than one

def get_static_manager():
    global __MANAGER
    if __MANAGER is None:
        try:
            __MANAGER = __InputManagerHandler()
        except Exception as e:
            raise TypeError from e
    return __MANAGER

keyboard.on_release(callback=__MANAGER.on_release,suppress=True)  #Listen the keyboard for a key release
keyboard.on_press(callback=__MANAGER.on_pressed,suppress=True)    #Listen the keyboard for a key press
