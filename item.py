# item.py
class Item:
    def __init__(self, name, description, is_locked=False, unlocks=None, contains=None):
        self.name = name
        self.description = description
        self.is_locked = is_locked
        self.unlocks = unlocks  # What this item unlocks (another item's name)
        self.contains = contains if contains is not None else []  # List of items

    def use(self, player, game):
        """Handles the logic of using an item."""
        if self.name == "weapon":
            return "You wield the makeshift weapon for defense."
        elif self.name == "key":
            # Find the chest in the current room
            for target_item in player.current_room.items:
                if target_item.name == "chest" and target_item.is_locked:
                    target_item.is_locked = False
                    target_item.contains.append(Item("gold", "A pile of gold!"))
                    return "You unlock the chest with the key!"
            return "There's nothing to unlock here."  # Key, but no lockable chest
        else:
            return f"You try to use the {self.name}, but nothing happens."

    def describe(self):
        """Return a description of the item."""
        return f"{self.name}: {self.description}"
