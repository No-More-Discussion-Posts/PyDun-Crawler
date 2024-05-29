class Inventory:
    def __init__(self):
        self.inventory = {}
    def add_item(self, item_id, item_name, item_count):
        self.inventory[item_id] = {"item name": item_name, "item_count": item_count}
    def update_item(self, item_id, item_count):
        if item_id in self.inventory:
            self.inventory[item_id] ["item_count"] = item_count
        else:
            #Shouldn't come up but extra logic just in case
            print("Item not found in inventory")