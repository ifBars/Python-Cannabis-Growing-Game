import os

class Utils:
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_quantity():
        while True:
            try:
                quantity = int(input(f"How many of this item do you want to buy? "))
                if quantity <= 0:
                    raise ValueError("Please enter a positive quantity.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}")
        return quantity
    
    def get_item_name(item_choice):
        item_mapping = {
            "1": "Pots",
            "2": "Soil",
            "3": "Nutrients",
            "4": "Trimming Scissors"
        }
        return item_mapping.get(item_choice, "Unknown Item")
    
    def game_over():
        print("\nGame over.")
        exit()

    def calculate_discount_multiplier(negotiation_skill):
        # Define the base discount multiplier and the rate of increase
        base_multiplier = 0.97  # 3% discount at the start
        increase_rate = 0.05  # 5% increase for each level of negotiation skill

        # Calculate the discount multiplier based on negotiation skill
        discount_multiplier = base_multiplier + (increase_rate * negotiation_skill)

        # Ensure the discount multiplier is not greater than 1 (100% discount)
        discount_multiplier = min(discount_multiplier, 1.0)

        return discount_multiplier

    def calculate_upgrade_cost(base_cost, negotiation_skill):
        # Get the discount multiplier based on negotiation skill
        discount_multiplier = Utils.calculate_discount_multiplier(negotiation_skill)

        # Calculate the discounted upgrade cost
        upgraded_cost = base_cost * discount_multiplier

        return upgraded_cost