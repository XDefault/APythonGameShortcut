import random

class Camera:

    __usedIndex = []
    #TODO Animated Camera Pos

    def __init__(self,name=None):
        self.__index = self.__generate_index()

        if name is None:
            self.__name = "Camera " + str(self.__index)
        else:
            self.__name = name

        self.__pos = [-6,0]
        self.__moveto = [0,0]

    def __generate_index(self):
        data = range(1,15000)
        new_id = random.sample(data,1)

        while self.__usedIndex.__contains__(new_id):
            new_id = random.sample(data,1)

        self.__usedIndex.append(new_id)
        return new_id

    def get_camera_name(self):
        return self.__name

    def get_camera_index(self):
        return self.__index

    def get_camera_pos(self):
        return self.__pos

    def get_camera_pos_x(self):
        return self.__pos[0]

    def get_camera_pos_y(self):
        return self.__pos[1]

    def set_camera_pos(self,pos):
        self.__moveto[0] = pos[0] - self.__pos[0]
        self.__moveto[1] = pos[1] - self.__pos[1]
        self.__pos = pos

    def set_camera_pos_x(self,posx):
        self.__moveto[0] = posx - self.__pos[0]
        self.__pos[0] = posx

    def set_camera_pos_y(self,posy):
        self.__moveto[1] = posy - self.__pos[1]
        self.__pos[1] = posy

    def get_moveto(self):        #This is meant to be used only by the render
        return self.__moveto

    def set_moveto(self,pos):    #This is meant to be used only by the render
        self.__moveto = pos

    def update(self):
        pass
    