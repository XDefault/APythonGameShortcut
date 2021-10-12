import json
import os
from enum import Enum

class Langs(Enum):
    EN = 0
    PT_BR = 1


__LANGUAGE = {}
__CURRENT_LANGUAGE = 0

__path_to_language_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'..','Lang','languages.json')
__path_to_language_json = os.path.normpath(__path_to_language_json)

print("Path: " + __path_to_language_json)

def __load_file():
    global __LANGUAGE
    try:
        f = open(__path_to_language_json)
        __LANGUAGE = json.load(f)
    except IOError:
        print("No File was found")

def get_text_by_value(value):
    try:
        word = __LANGUAGE[__CURRENT_LANGUAGE][value]
        return word
    except ValueError as e:
        print(e)
        return "Language Value Not Found"

def change_language(new_language:Langs):
    global __CURRENT_LANGUAGE
    __CURRENT_LANGUAGE = new_language.value


__load_file()
