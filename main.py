from raylibpy import *
from game.player import player
from server.rooms import rooms
import time

Host = None
playerName = input("Enter Your Name: ")
checkHost = input("Are you host?: ")

if checkHost == "y":
    Host=True
if checkHost == "n":
    Host = False
roomID = input("Enter roomID: ")

def game(host):
    init_window(600, 600, "test multiplayer")
    set_target_fps(60)
    Rooms = rooms()
    Player = player(Rooms)
    if host:
        Player.Start(playerName)
        Rooms.createRoom(roomID, playerName, Player.x, Player.y, Player.speed)
    else:
        Player.Start(playerName)
        Rooms.loadRoom(roomID, playerName, Player.x, Player.y, Player.speed)


    while not window_should_close():
        Player.Update(roomID)
        Rooms.refreshData()
        #time.sleep(0.01)
        begin_drawing()
        
        clear_background(GRAY)
        if roomID in Rooms.data["rooms"]:
            for playerData in Rooms.data["rooms"][roomID]["players"].values():
                draw_rectangle(playerData["x"], playerData["y"], 15, 15, RED)
        end_drawing()
    close_window()

if __name__ == '__main__':
    if Host:
        game(True)
    else:
        game(False)