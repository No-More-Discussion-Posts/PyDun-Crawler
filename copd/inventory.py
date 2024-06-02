
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

class Equipped:
    def __init__(self):
        self.equipped = {'Helm' : 'No Item', 'Armor': 'No Item', 'Weapon' : 'No Item'}

    def equip_item(self, item_part, item_name):
        self.equipped[item_part] = item_name
    
    def unequip_item(self, item_part, item_name):
        if item_name in self.equipped:
            self.equipped[item_part] = 'No Item'
        else:
            pass
    