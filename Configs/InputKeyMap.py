from classes.InputSystem.Keys import Key


class __InputMap:
    keys = [Key("up","w"),Key("down","s"),Key("left","a"),Key("right","d")]

    def get_key_by_action_name(self,action):
        try:
            value = ""
            for k in self.keys:
                if k.action_name == action:
                    value = k.key_input
                    break

        except ValueError:
            value = ""

        return value

    def get_action_name_by_key(self,key_to_get):
        try:
            value = ""
            for k in self.keys:
                if k.key_input == key_to_get:
                    value = k.action_name
                    break

        except ValueError:
            value = ""

        return value

    def change_input_with_action_name(self,action,new_input):
        try:
            key_list_size = len(self.keys)
            index = 0
            while key_list_size > 0:
                if self.keys[index].action_name == action:
                    self.keys[index].key_input = new_input
                    break
                else:
                    key_list_size -= 1
                    index += 1
        except ValueError:
            print("ERROR: No action has been found")

__STATIC_INPUT_MAP = __InputMap()

def get_static_map():
    global __STATIC_INPUT_MAP
    if __STATIC_INPUT_MAP is None:
        try:
            __STATIC_INPUT_MAP = __InputMap()
        except Exception as e:
            raise TypeError from e
    return __STATIC_INPUT_MAP
