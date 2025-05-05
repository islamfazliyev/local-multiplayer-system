from raylibpy import *
from game.player import player
import socket
import json
import threading

#Host = None
playerName = input("Enter Your Name: ")
#checkHost = input("Are you host?: ")

# if checkHost == "y":
#     Host=True
# if checkHost == "n":
#     Host = False
roomID = input("Enter roomID: ")

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 5555))
        self.data = {}
        self.lock = threading.Lock()
        
        self.recv_thread = threading.Thread(target=self.receive_data)
        self.recv_thread.daemon = True
        self.recv_thread.start()
    def receive_data(self):
        while True:
            try:
                response = self.client.recv(1024).decode()
                if response:
                    with self.lock:
                        self.data = json.loads(response)
            except Exception as e:
                print(f"Sunucu bağlantısı koptu: {e}")
                break
    
    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())
        except Exception as e:
            print(f"Gönderme hatası: {e}")

def game():
    init_window(600, 600, "test multiplayer")
    set_target_fps(60)
    net = Network()
    Player = player()
    net.send({
        'type': 'join',
        'roomID': roomID,
        'name': playerName,
        'x': Player.x,
        'y': Player.y
    })


    while not window_should_close():
        Moved = False
        if is_key_down(KEY_W):
            Player.y-=Player.speed
            Moved = True

        if is_key_down(KEY_S):
            Player.y+=Player.speed
            Moved = True

        if is_key_down(KEY_A):
            Player.x-=Player.speed
            Moved = True

        if is_key_down(KEY_D):
            Player.x+=Player.speed
            Moved = True

        if Moved:
            net.send({
                'type': 'update',
                'roomID': roomID,
                'name': playerName,
                'x': Player.x,
                'y': Player.y
            })
        
        begin_drawing()
        
        clear_background(GRAY)
        with net.lock:
            print("alinan veri:", net.data)
            if 'players' in net.data:
                print("Players:", net.data["players"])

                for name, pos in net.data['players'].items():
                    print(f"positions: {int(pos[0])}, {int(pos[1])}")
                    draw_rectangle(int(pos[0]), int(pos[1]), 15, 15, RED)
        end_drawing()
    close_window()

if __name__ == '__main__':
    game()
    # if Host:
    #     game(True)
    # else:
    #     game(False)