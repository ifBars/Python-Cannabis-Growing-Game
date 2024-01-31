import json
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Shop:
    def __init__(self, inventory, cash, level):
        self.update_shop(inventory, cash, level)

    def update_shop(self, inventory, cash, level):
        self.inventory = inventory
        self.cash = cash
        self.level = level

    def buy_item(self, item_type, item_name, quantity, selected_strain=None, discounted_cost=None):
        item_mapping = {
            "1": ("Pots", 20),
            "2": ("Soil", 10),
            "3": ("Nutrients", 15),
            "4": ("Trimming Scissors", 30),
            "Seeds": (f"{item_name} Seed(s)", discounted_cost) if selected_strain and discounted_cost else None
        }

        if item_type in item_mapping:
            selected_item, price = item_mapping[item_type]

            if item_type != "Seeds":
                total_cost = price * quantity
            else:
                total_cost = discounted_cost * quantity

            if self.cash >= total_cost:
                self.cash -= total_cost

                # Handling items that are not seeds separately
                if item_type != "Seeds":
                    self.inventory[item_name] += quantity
                else:
                    # Handling seeds
                    self.inventory["Seeds"].setdefault(item_name, 0)
                    self.inventory["Seeds"][item_name] += quantity

                print(f"You bought {quantity} {selected_item} for ${total_cost}.")
                time.sleep(1)
                return True
            else:
                print("Not enough cash to buy this item.")
                time.sleep(1)
                return False
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)
            return False
