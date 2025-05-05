import socket
import threading
import json

class GameServer:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.rooms = {}

        
    
    def broadcast(self, roomID, data):
        try:
            # Tuple'ı listeye çevir
            formatted_data = {
                "players": {
                    name: [int(pos[0]), int(pos[1])]
                    for name, pos in data["players"].items()
                }
            }
            message = json.dumps(formatted_data).encode()
            for client in self.clients:
                if client['roomID'] == roomID:
                    client['conn'].sendall(message)
        except Exception as e:
            print(f"Yayın hatası: {e}")
    
    def handleClient(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                
                message = json.loads(data) 
                roomID = message['roomID']
                
                if message['type'] == 'join':
                    self.clients.append({'conn': conn, 'roomID': roomID})
                    if roomID not in self.rooms:
                        self.rooms[roomID] = {'players': {}}
                    self.rooms[roomID]['players'][message['name']] = (message['x'], message['y'])
                    self.broadcast(roomID, self.rooms[roomID])
                
                elif message['type'] == 'update':
                    self.rooms[roomID]['players'][message['name']] = (message['x'], message['y'])
                    self.broadcast(roomID, self.rooms[roomID])
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
        
    def run(self):
        print("Sunucu başlatıldı...")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handleClient, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = GameServer()
    server.run()