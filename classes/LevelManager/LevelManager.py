
class __LevelManager:

    __levels = []
    __current_level = None
    __current_level_index = -9999
    __render = None

    def add_level_to_list(self,level):
        self.__levels.append(level)

    def load_level(self,level_index):
        print("   '->Loading: " + self.__levels[level_index].name)

        if self.__current_level is not None:                    #<--May be remove
            self.unload_level(self.__current_level_index)

        self.__levels[level_index].set_render_manager(self.__render)
        self.__init_level_components(level_index)

        self.__current_level = self.__levels[level_index]
        self.__current_level_index = level_index

    def load_level_with_index(self,search_index):
        index = 0
        print("   '->Searching Level with internal index: " + str(search_index))
        for l in self.__levels:
            print("      '->Level Index " + str(l.index) + ": Checked")
            if l.index == search_index:
                self.load_level(index)
                return

            index += 1

        print("      '->No Level with Index "+ str(search_index)+" was Found")

    def load_level_with_name(self,search_name=str):
        index = 0
        print("   '->Searching Level with Name: " + search_name)
        for l in self.__levels:
            print("      '->Level Name - " + str(l.name) + ": Checked")
            if l.name == search_name:
                self.load_level(index)
                return

            index += 1

        print("      '->No Level with Name "+ search_name +" was Found")

    def unload_level(self,level_index):
        print("   '->Unload Level: " + self.__levels[level_index].name)
        self.__levels[level_index].unload_entities_on_level()

    def unload_level_with_name(self,search_name=str):
        index = 0
        print("   '->Searching Level with Name: " + search_name)
        for l in self.__levels:
            print("      '->Level Name - " + str(l.name) + ": Checked")
            if l.name == search_name:
                self.unload_level(index)
                return

            index += 1

        print("      '->No Level with Name "+ search_name +" was Found")

    def unload_level_with_index(self,search_index):
        index = 0
        print("   '->Searching Level with internal index: " + str(search_index))
        for l in self.__levels:
            print("      '->Level Index " + str(l.index) + ": Checked")
            if l.index == search_index:
                self.unload_level(index)
                return

            index += 1

        print("      '->No Level with Index "+ str(search_index)+" was Found")

    def __init_level_components(self,level_index):
        print("      '->Init Level: " + self.__levels[level_index].name)
        self.__levels[level_index].init_objects()
        #raise NotImplementedError

    def arrange_level_order(self):
        print("\nLevelManager")
        print("   '->Levels Rearranged")
        self.__levels.sort(key=lambda  n: n.get_index())
        print("   '->Current Level Order: " + str([str(e.index.__str__()+":"+e.name) for e in self.__levels]))

    def update_level_entities(self):
        self.__current_level.update_entities()

    def set_render_manager(self,render):
        self.__render = render

__MANAGER = __LevelManager()


def get_static_manager():
    global __MANAGER
    if __MANAGER is None:
        try:
            __MANAGER = __LevelManager()
        except Exception as e:
            raise TypeError from e
    return __MANAGER
    