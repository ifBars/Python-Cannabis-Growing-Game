import json
import random
import time
import os
from shop import Shop
from weed_plant import WeedPlant
from skills import Skills
from utils import Utils
        
class WeedGame:
    
    BUY_SEEDS_PROMPT = "How many seeds of {strain_name} do you want to buy? "
    BUY_SEEDS_ERROR_MESSAGE = "Please enter a positive quantity."
    
    def __init__(self):
        self.inventory = {
            "Pots": 0,
            "Soil": 0,
            "Nutrients": 0,
            "Trimming Scissors": 0,
            "Seeds": {}
        }
        self.cash = 1000
        self.level = {
            "player": 1,
            "light_management": 1,
            "nutrient_management": 1,
            "water_management": 1,
            "negotiation": 1,
            "charisma": 1,
            "trimming": 1,
            "harvesting": 1
        }
        self.xp = {
            "player": 0,
            "light_management": 0,
            "nutrient_management": 0,
            "water_management": 0,
            "negotiation": 0,
            "charisma": 0,
            "trimming": 0,
            "harvesting": 0
        }
        self.buyers = {
            "casual": {"preference": "Balanced", "pay_multiplier": 1.0},
            "medical": {"preference": "High CBD", "pay_multiplier": 1.2},
            "recreational": {"preference": "High THC", "pay_multiplier": 1.5}
        }
        self.strains = self.load_strains()
        self.current_strain = None
        self.plants = []
        self.max_plants = 2
        self.shop = Shop(self.inventory, self.cash, self.level)
        self.skills = Skills(self.level, self.xp)

    def update_game(self, inventory, cash, level):
        self.inventory = inventory
        self.cash = cash
        self.level = level

    def load_strains(self):
        with open("strains.json", "r") as file:
            strains_data = json.load(file)
        return strains_data

    def display_strains(self):
        print("\nAvailable Strains:")
        for strain in self.strains:
            print(f"- {strain['name']} (Type: {strain['type']}, THC: {strain['thc']}%, CBD: {strain['cbd']}%)")

    def display_menu(self):
        Utils.clear_screen()
        print(f"\n=== Weed Growing Simulator ===\nLevel: {self.level['player']} | Cash: ${self.cash} | Items: {self.inventory}")
        print("1. Buy items\n2. Buy seeds\n3. Plant seeds\n4. Harvest plants\n5. Sell plants\n6. Display Plants\n7. Upgrades\n8. Save game\n9. Load Game\n10. Quit")
        
    def get_user_input(self, prompt, error_message):
        while True:
            try:
                value = input(prompt)
                return value
            except ValueError as e:
                print(f"Invalid input: {e}")
                print(error_message)
        
    def buy_seeds(self, selected_strain):
        if selected_strain:
            strain_name = selected_strain['name']

            # Calculate seed price based on THC, CBD percentages, and negotiation skill level
            base_price = int(((selected_strain['thc'] * 2) + selected_strain['cbd']) * 4 / 2)
            discounted_price = int(base_price * (1 - self.level['negotiation'] / 10))  # Apply negotiation skill discount

            # Display the price next to the strain
            print(f"Price per seed of {strain_name}: ${discounted_price}")

            quantity = int(self.get_user_input(self.BUY_SEEDS_PROMPT.format(strain_name=strain_name),
                                   self.BUY_SEEDS_ERROR_MESSAGE))

            self.current_strain = selected_strain  # Set current_strain before updating inventory

            while True:
                total_cost = discounted_price * int(quantity)
                if self.cash >= total_cost:
                    self.shop.update_shop(self.inventory, self.cash, self.level)
                    if self.shop.buy_item("Seeds", strain_name, quantity, selected_strain, discounted_price):
                        # Update the WeedGame's internal state after a successful purchase
                        self.inventory = self.shop.inventory
                        self.cash = self.shop.cash
                        self.level = self.shop.level
                        self.skills.add_xp("negotiation", 25)
                        break
                    else:
                        print("An error occurred while buying seeds. Please choose another option.")
                        break
                else:
                    print(f"Not enough cash to buy {quantity} seeds. Please choose another option.")
                    choice = input("Do you want to buy more seeds? (y/n): ").lower()
                    if choice != 'y':
                        break
                    else:
                        continue
        else:
            print("Invalid strain selection. Please try again.")

    def sell_plant(self):
        if self.plants:
            preferred_buyer = None
            max_thc_percentage = 25.0
            min_cbd_percentage = 0.6
            total_earnings = 0

            for plant in self.plants:
                if plant.trimmed:  # Check if the plant is harvested
                    thc_percentage = plant.strain['thc']
                    cbd_percentage = plant.strain['cbd']

                    # Determine the preferred buyer based on THC and CBD percentages
                    if thc_percentage >= max_thc_percentage:
                        preferred_buyer = "recreational"
                    elif cbd_percentage >= min_cbd_percentage:
                        preferred_buyer = "medical"
                    else:
                        preferred_buyer = "casual"

                    base_price = int((thc_percentage + cbd_percentage) * 10 / 2)
                    growth_bonus = int((plant.height - 10) * 5)  # Bonus for well-grown plants
                    negotiation_bonus = int(base_price * (self.level['negotiation'] / 10))
                    charisma_bonus = int(base_price * (self.level['charisma'] / 10))
                    sell_price = int((base_price + growth_bonus + negotiation_bonus + charisma_bonus) * self.buyers[preferred_buyer]["pay_multiplier"])

                    total_earnings += sell_price

            if total_earnings > 0:
                print(f"\nYou sold your trimmed buds to {preferred_buyer} for ${total_earnings}.")
                self.cash += total_earnings
                self.plants = []
                self.skills.add_xp("charisma", total_earnings / 10)
            else:
                print("No trimmed plants to sell. Grow, harvest, and trim some plants first.")
        else:
            print("No plants to sell. Grow some plants first.")
        time.sleep(3)

    def grow_plants(self):
        if not self.inventory["Seeds"]:
            print("No seeds available. Buy seeds first.")
            time.sleep(3)
            return

        print("\nPlanting your seeds...")
        time.sleep(5)

        seeds_to_remove = []

        for seed_type, seed_count in self.inventory["Seeds"].items():
            # Iterate through each type/strain of seed in the inventory
            for _ in range(min(self.max_plants - len(self.plants), seed_count)):
                selected_strain = next((strain for strain in self.strains if strain['name'].lower() == seed_type.lower()), None)

                if selected_strain:
            
                    if self.inventory["Pots"] < 1 or self.inventory["Soil"] < 1 or self.inventory["Nutrients"] < 1:
                        print("Not enough resources to grow a new plant. Make sure you have enough pots, soil, and nutrients.")
                        time.sleep(3)
                        return
            
                    light_factor = random.uniform(0.7 + (self.level['light_management'] / 10), 1.3 + (self.level['light_management'] / 10))
                    water_factor = random.uniform(0.8 + (self.level['water_management'] / 10), 1.2 + (self.level['water_management'] / 10))
                    nutrient_factor = random.uniform(0.9 + (self.level['nutrient_management'] / 10), 1.1 + (self.level['nutrient_management'] / 10))

                    new_plant = WeedPlant(selected_strain)
                    new_plant.grow(light_factor, water_factor, nutrient_factor)
                    print(f"\n{new_plant.strain['name']} has been planted!")
                    new_plant.display_status()
                    time.sleep(3)

                    # Deduct resources from the player's inventory
                    self.inventory["Pots"] -= 1
                    self.inventory["Soil"] -= 1
                    self.inventory["Nutrients"] -= 1
                    self.inventory["Seeds"][seed_type] -= 1
                
                    if self.inventory["Seeds"][seed_type] == 0:
                        seeds_to_remove.append(seed_type)

                    self.plants.append(new_plant)

                else:
                    print(f"Invalid seed type: {seed_type}. Skipping planting.")

        # Remove seeds with count == 0 from the inventory
        for seed_type in seeds_to_remove:
            del self.inventory["Seeds"][seed_type]

        print("\nAll available seeds have been planted.")
        time.sleep(2)

    def upgrade_max_plants(self):
        upgrade_cost = Utils.calculate_upgrade_cost(500 * self.max_plants, self.level['negotiation'])
        if self.cash >= upgrade_cost:
            self.max_plants += 1
            self.cash -= upgrade_cost
            print(f"You upgraded your maximum number of plants to {self.max_plants}.")
            time.sleep(3)
        else:
            print("Upgrade failed. Not enough cash.")
            time.sleep(3)

    def main_loop(self):
        milestones = {
            5: "You've reached level 5! Your negotiation skill has increased.",
            10: "You've reached level 10! Your charisma skill has increased.",
            20: "You've reached level 20! Your trimming skill has increased."
        }

        while True:
            self.display_menu()

            choice = input("Choose an option: ")

            if choice == "1":
                self.buy_items_menu()
            elif choice == "2":
                self.buy_seeds_menu()
            elif choice == "3":
                self.grow_plants_menu()
            elif choice == "4":
                self.harvest_plant_menu()
            elif choice == "5":
                self.sell_plant_menu()
            elif choice == "6":
                self.view_plants_menu()
            elif choice == "7":
                self.upgrades_menu()
            elif choice == "8":
                self.save_game_menu()
            elif choice == "9":
                self.load_game_menu()
            elif choice == "10":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def grow_plants_menu(self):
        if len(self.plants) < self.max_plants:
            self.grow_plants()
        else:
            print(f"You can only grow up to {self.max_plants} plants at a time. Harvest some plants first.")
            time.sleep(3)

    def harvest_plant_menu(self):
        ready_to_harvest = [plant for plant in self.plants if plant.height >= 30]

        if ready_to_harvest:
            for plant in ready_to_harvest:
                harvesting_time = int(5 / (self.level['harvesting'] / 2))
                print(f"\nHarvesting {plant.strain['name']}... This will take {harvesting_time} seconds.")
                time.sleep(harvesting_time)
                print(f"\nHarvest complete for {plant.strain['name']}! You can now trim the plant.")
                plant.harvested = True
                self.skills.add_xp("harvesting", 25)
                plant.display_status()
                time.sleep(1)
        else:
            print("No plant is ready to harvest. Wait until they reach a height of 30 cm.")
            time.sleep(3)

    def sell_plant_menu(self):
        if self.plants:
            self.sell_plant()
            self.skills.add_xp("charisma", 25)
        else:
            print("No plants to sell. Grow some plants first.")
            time.sleep(3)

    def view_plants_menu(self):
        if self.plants:
            print("\n=== Your Plants ===")
            for index, plant in enumerate(self.plants, start=1):
                print(f"\nPlant {index}: {plant.strain['name']}")
                plant.display_status()

                # Check if the plant has been harvested
                if not plant.harvested:
                    care_choice = input("\nDo you want to take care of this plant? (w)ater, (l)ighting, (n)utrients, (s)kip or press enter: ").lower()
                    if care_choice == 'w':
                        if not plant.grow(.25, 1.3, .25):
                            self.plants.pop(plant)
                        else:
                            self.skills.add_xp("water_management", 25)
                    elif care_choice == 'l':
                        if not plant.grow(1.2, .25, .25):
                            self.plants.pop(plant)
                        else:
                            self.skills.add_xp("light_management", 25)
                    elif care_choice == 'n':
                        if not plant.grow(.25, .25, 1.5):
                            self.plants.pop(plant)
                        else:
                            self.skills.add_xp("nutrient_management", 25)
                    elif care_choice == 's':
                        if not plant.grow(0, 0, 0):
                            self.plants.pop(plant)
                    elif care_choice == '':
                        if not plant.grow(0, 0, 0):
                            self.plants.pop(plant)
                elif not plant.trimmed:
                    care_choice = input("\nDo you want to trim this harvested plant? (y/n): ").lower()
                    if care_choice == 'y':
                        trimming_level = input("Choose trimming level: (1) Light Trim, (2) Heavy Trim, (3) Selective Trim: ")

                        # Apply trimming effects based on the chosen level
                        if trimming_level == '1':
                            trimming_time = int(random.randint(8, 12) / (self.level['trimming'] / 2))
                            plant.trim_light(trimming_time)
                            self.skills.add_xp("trimming", 25)
                        elif trimming_level == '2':
                            trimming_time = int(random.randint(14, 18) / (self.level['trimming'] / 2))
                            plant.trim_heavy(trimming_time)
                            self.skills.add_xp("trimming", 25)
                        elif trimming_level == '3':
                            trimming_time = int(random.randint(12, 20) / (self.level['trimming'] / 2))
                            plant.trim_selective(trimming_time)
                            self.skills.add_xp("trimming", 25)
                        else:
                            print("Invalid trimming level. No trimming applied.")

                        time.sleep(1)
        else:
            print("You have no plants. Grow some plants first.")
            time.sleep(1)

    def upgrades_menu(self):
        if self.max_plants < 25:
            print("\n=== Upgrades ===")
            print(f"1. Upgrade Maximum Plants to {self.max_plants + 1} (${Utils.calculate_upgrade_cost(500 * self.max_plants, self.level['negotiation'])})")
            print("2. Back to main menu")

            upgrade_choice = input("What upgrade do you want to purchase? ")

            if upgrade_choice == "1":
                self.upgrade_max_plants()
            elif upgrade_choice == "2":
                return
            else:
                print("Invalid choice. Please try again.")
        else:
            print("\n=== Upgrades ===")
            print("All Upgrades Bought")
            print("1. Back to main menu")


        
    def buy_seeds_menu(self):
        Utils.clear_screen()
        self.display_strains()

        while True:
            strain_name_input = input("\nSelect a strain to buy seeds: ").capitalize()
            selected_strain = next((strain for strain in self.strains if strain['name'].lower() == strain_name_input.lower()), None)

            if selected_strain:
                self.buy_seeds(selected_strain)
            else:
                print("Invalid strain name. Please try again.")
                continue  # Added continue to break out of the loop in case of an invalid strain name

            # Allow the user to buy more seeds or go back to the main menu
            choice = input("Do you want to buy more seeds? (y/n): ").lower()
            if choice != 'y':
                break

    def buy_items_menu(self):
        while True:
            Utils.clear_screen()
            print(f"\n=== Shop ===\nLevel: {self.level['player']} | Cash: ${self.cash} | Items: {self.inventory}")
            print("1. Pot ($20)\n2. Soil ($10)\n3. Nutrients ($15)\n4. Trimming Scissors ($30)\n5. Back to main menu")

            shop_choice = input("What do you want to buy? ")

            if shop_choice == "5":
                break
            else:
                item_name = Utils.get_item_name(shop_choice)

                if item_name in self.inventory:
                    quantity = Utils.get_quantity()
                    self.shop.update_shop(self.inventory, self.cash, self.level)
                    self.shop.buy_item(shop_choice, item_name, quantity)
                    self.update_cash(self.shop.cash)
                    self.shop.update_shop(self.inventory, self.cash, self.level)
                else:
                    print(f"{shop_choice} is not a valid choice. Please choose another item.")
                    time.sleep(1)

    def buy_item_menu(self, item_choice, item_name):
        while True:
            try:
                quantity = int(input(f"How many of {item_name} do you want to buy? "))
                if quantity <= 0:
                    raise ValueError("Please enter a positive quantity.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}")

        item_mapping = {
            "1": ("Pots", 20),
            "2": ("Soil", 10),
            "3": ("Nutrients", 15),
            "4": ("Trimming Scissors", 30),
        }

        if item_choice in item_mapping:
            selected_item, price = item_mapping[item_choice]
            total_cost = price * quantity
            if self.cash >= total_cost:
                self.cash -= total_cost
                self.update_cash(self.shop.cash)
                self.shop.update_shop(self.inventory, self.cash, self.level)

                # Handling items that are not seeds separately
                if selected_item != "Seeds":
                    self.inventory[selected_item] += quantity
                else:
                    # Handling seeds
                    strain_name = self.current_strain['name']
                    self.inventory["Seeds"].setdefault(strain_name, 0)
                    self.inventory["Seeds"][strain_name] += quantity

                print(f"You bought {quantity} {item_name}.")
                time.sleep(3)
            else:
                print("Not enough cash to buy this item.")
                time.sleep(3)
        else:
            print("Invalid choice. Please try again.")

    def save_game_menu(self):
        print("\n=== Save Game ===")
        for slot in range(1, 4):
            save_file = f"save_game_{slot}.json"
            print(f"{slot}. Save to Slot {slot} ({save_file})")

        print("4. Back to main menu")

        slot_choice = input("Choose a slot to save the game: ")

        if slot_choice.isdigit() and 1 <= int(slot_choice) <= 3:
            slot_number = int(slot_choice)
            save_file = f"save_game_{slot_number}.json"
            self.save_game(save_file, slot_number)
        elif slot_choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)
        
    def load_game_menu(self):
        print("\n=== Load Game ===")
        for slot in range(1, 4):
            save_file = f"save_game_{slot}.json"
            if os.path.exists(save_file):
                print(f"{slot}. Load from Slot {slot} ({save_file})")
            else:
                print(f"{slot}. Slot {slot} is empty")

        print("4. Back to main menu")

        slot_choice = input("Choose a slot to load the game: ")

        if slot_choice.isdigit() and 1 <= int(slot_choice) <= 3:
            slot_number = int(slot_choice)
            save_file = f"save_game_{slot_number}.json"
            if os.path.exists(save_file):
                self.load_game(save_file, slot_number)
            else:
                print(f"Slot {slot_number} is empty. Choose another slot or save a game to this slot.")
                time.sleep(1)
        elif slot_choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

    def update_cash(self, cash):
        self.cash = cash

    def save_game(self, save_file, slot_number):
        data = {
            "inventory": self.inventory,
            "cash": self.cash,
            "level": self.level,
            "xp": self.xp,
            "strains": self.strains,
            "current_strain": self.current_strain,
            "plants": [plant.serialize() for plant in self.plants] if self.plants else None,
            "max_plants": self.max_plants
        }
        with open(save_file, "w") as file:
            json.dump(data, file)
        print(f"Game saved to Slot {slot_number} Filename ({save_file}).")
        time.sleep(1)

    def load_game(self, save_file, slot_number):
        if os.path.exists(save_file):
            with open(save_file, "r") as file:
                data = json.load(file)

            self.inventory = data["inventory"]
            self.cash = data["cash"]
            self.level = data["level"]
            self.xp = data["xp"]
            self.strains = data["strains"]
            self.current_strain = data["current_strain"]
            self.plants = [WeedPlant.deserialize(plant_data) for plant_data in data["plants"]] if data["plants"] else []
            self.max_plants = data["max_plants"]

            # Update the shop instance with the current state
            self.shop.update_shop(self.inventory, self.cash, self.level)

            print(f"Game loaded from Slot {slot_number} Filename ({save_file}).")
            time.sleep(1)
        else:
            print(f"Slot {slot_number} is empty. Choose another slot or save a game to this slot.")
            time.sleep(1)