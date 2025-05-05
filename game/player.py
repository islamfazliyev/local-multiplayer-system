from raylibpy import *


class player:
    def __init__(self):
        self.name = ""
        self.x = 0
        self.y = 0
        self.speed = 10

    def Start(self, name):
        self.name = name

    # def Update(self, id):
    #     Moved = False
    #     if is_key_down(KEY_W):
    #         self.y-=self.speed
    #         Moved = True

    #     if is_key_down(KEY_S):
    #         self.y+=self.speed
    #         Moved = True

    #     if is_key_down(KEY_A):
    #         self.x-=self.speed
    #         Moved = True

    #     if is_key_down(KEY_D):
    #         self.x+=self.speed
    #         Moved = True

    #     if Moved:
    #         self.Rooms.updatePlayer(id, self.name, self.x, self.y)
    
    # def Draw(self):
    #     draw_rectangle(self.x,self.y,15,15,RED)