from ghh_parameters import INIT_NUM_ITEM, MAX_NUM_ITEM


class Place:
    def __init__(self, name, initial_buyable, selling_info, not_start=True):
        self.name = name
        self.speciality = initial_buyable
        self.selling_info = selling_info
        self.player_can_stop = not_start
        self.player_can_buy = not_start
        self.player_can_sell = not_start
        if not_start:
            self.inventory = [initial_buyable] * INIT_NUM_ITEM
        else:
            self.inventory = None

    def player_buy(self, name, quantity):
        if self.player_can_buy:
            # Check if there is enough goods
            if self.inventory.count(name) < quantity:
                print("The number of {} is less than {}. You cannot buy that much!".format(name, quantity))
            else:
                # Remove certain amount of goods from the inventory
                for i in range(quantity):
                    self.inventory.remove(name)

                # Place become 'salable' after buying
                self.player_can_sell = True

                # No longer 'buyable' if the inventory is empty
                if len(self.inventory) < 1:
                    self.player_can_buy = False

    def player_sell(self, name, quantity):
        if self.player_can_sell:
            # Check if there is enough slots
            if len(self.inventory) + quantity > MAX_NUM_ITEM:
                print("The number of slots is less than {}. You cannot sell that much!".format(quantity))
            else:
                # Add goods to the inventory
                self.inventory = self.inventory + [name] * quantity

                # Place become 'buyable' after selling
                self.player_can_buy = True

                # No longer 'salable' if the inventory is full
                if len(self.inventory) >= MAX_NUM_ITEM:
                    self.player_can_sell = False
