import json
import os
from enum import Enum

class Langs(Enum):
    EN = 0
    PT_BR = 1


__language = {}
__currentLanguage = 0

__pathToLanguageJson = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'..','Lang','languages.json')
__pathToLanguageJson = os.path.normpath(__pathToLanguageJson)

print("Path: " + __pathToLanguageJson)

def __LoadFile():
    global __language
    try:
        f = open(__pathToLanguageJson)
        __language = json.load(f)
    except IOError:
        print("No File was found")

def GetTextByValue(value):
    try:
        word = __language[__currentLanguage][value]
        return word
    except:
        return "Language Value Not Found"

def ChangeLanguage(newLanguage:Langs):
    global __currentLanguage
    __currentLanguage = newLanguage.value
    
    
__LoadFile()