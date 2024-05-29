class Inventory:
    def __init__(self):
        self.inventory = {}
    def add_item(self, item_name, item_count):
        self.inventory[item_name] = item_count
    def update_item(self, item_name, item_count):
        if item_name in self.inventory:
            self.inventory[item_name] += item_count
        else:
            self.add_item(item_name, item_count)
    def use_item(self, item_name, item_count):
        self.inventory[item_name] -= item_count
        if self.inventory[item_name] == 0:
            self.inventory.pop(item_name)