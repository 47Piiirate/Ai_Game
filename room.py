# room.py
class Room:
    def __init__(self, name, description, exits, items=None):
        self.name = name
        self.description = description
        self.exits = exits  # Dictionary: direction -> room name
        self.items = items if items is not None else []  # List of Item objects

    def __str__(self):
        return self.name

    def add_exit(self, direction, room_name):
        """Adds an exit to the room."""
        if direction not in self.exits:
            self.exits[direction] = room_name
        else:
            raise ValueError(f"Exit {direction} already exists.")

    def remove_exit(self, direction):
        """Removes an exit from the room."""
        if direction in self.exits:
            del self.exits[direction]
        else:
            raise ValueError(f"Exit {direction} does not exist.")
