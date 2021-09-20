from classes.InputSystem.InputClass import Input
from classes.InputSystem.Keys import Key
import keyboard


class __InputMap:
    keys = [Key("up","w"),Key("down","s"),Key("left","a"),Key("right","d")]

    def GetKeyByActionName(self,action):
        try:
            value = ""
            for k in self.keys:
                if(k.actionName == action):
                    value = k.Input
                    break

        except:
            value = ""
        
        return value

    def GetActionNameByKey(self,keyToGet):
        try:
            value = ""
            for k in self.keys:
                if(k.Input == keyToGet):
                    value = k.actionName
                    break
        
        except:
            value = ""

        return value

    def ChangeInputWithActionName(self,action,newInput):
        try:
            keyListSize = len(self.keys)
            index = 0
            while(keyListSize > 0):
                if(self.keys[index].actionName == action):
                    self.keys[index].Input = newInput
                    break
                else:
                    keyListSize -= 1
                    index += 1
        except:
            print("ERROR: No action has been found")

__staticInputMap = __InputMap()

def GetStaticMap():
    global __staticInputMap
    if(__staticInputMap == None):
        try:
            __staticInputMap = __InputMap()
        except:
            raise TypeError
    return __staticInputMap