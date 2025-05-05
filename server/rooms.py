import json


class rooms:
    def __init__(self):
        self.data = {
        "rooms": {}
        }

    def createRoom(self, id, playerName, startX, startY, startSpeed):
        import os
        
        self.data["rooms"][id] = {
            "players": {
                playerName: {
                    "x": startX,
                    "y": startY,
                    "speed": startSpeed
                }
            }
        }

        print(f"room {id} created")
        print(json.dumps(self.data, indent=4))

        # Debug: Print the save path
        save_path = os.path.join(os.getcwd(), "db.json")
        print(f"Saving to: {save_path}")

        with open("db.json", "w") as f:
            json.dump(self.data, f, indent=4)
            print("saved")


    def loadRoom(self, id, playerName, startX, startY, startSpeed):
        import os
        save_path = os.path.join(os.getcwd(), "db.json")
        
        try:
            # FIRST: Load the LATEST data from JSON file
            with open("db.json", "r") as f:
                self.data = json.load(f)  # Refresh data from disk
        except FileNotFoundError:
            print("Error: db.json not found. Host must create the room first.")
            return

        # NOW check if room exists with FRESH data
        if id in self.data["rooms"]:
            # Add player to existing room
            self.data["rooms"][id]["players"][playerName] = {
                "x": startX,
                "y": startY,
                "speed": startSpeed
            }
            print(f"Joined room {id}")
            
            # Save updated data back to JSON
            with open("db.json", "w") as f:
                json.dump(self.data, f, indent=4)
                print(f"Saved updated room {id} to db.json")
                
        else:
            # Critical fix: DON'T save data if room doesn't exist
            print(f"Room {id} does not exist. Ask the host to create it first.")
    
    def updatePlayer(self, id, name, x, y):
        import os
        import tempfile
        save_path = os.path.join(os.getcwd(), "db.json")

        try:
            with open("db.json", "r") as f:
                latest_data = json.load(f)
            self.data = latest_data 
        except FileNotFoundError:
            print("Error: db.json not found.")
            return

        if id in self.data["rooms"]:
            if name in self.data["rooms"][id]["players"]:
                self.data["rooms"][id]["players"][name]["x"] = x
                self.data["rooms"][id]["players"][name]["y"] = y
                print(f"Updated {name}'s position in room {id}")
            else:
                print(f"Player {name} not found in room {id}")
                return
        else:
            print(f"Room {id} does not exist.")
            return

        with open("db.json", "w") as f:
            json.dump(self.data, f, indent=4)
            print(f"Saved to: {save_path}")
        temp_path = os.path.join(tempfile.gettempdir(), "temp_db.json")
        with open(temp_path, "w") as f:
            json.dump(self.data, f, indent=4)
        
        # Replace the old file atomically
        os.replace(temp_path, "db.json")
        print(f"Saved {name}'s position")
    
    def refreshData(self):
        
        try:
            with open("db.json", "r") as f:
                content = f.read().strip()
                if not content:
                    print("json is empty, Skipping refresh")
                    return
                self.data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            print(f"Refresh failed: {str(e)}. Retrying next frame.")
        except FileNotFoundError:
            print("db.json not found (refresh failed)")