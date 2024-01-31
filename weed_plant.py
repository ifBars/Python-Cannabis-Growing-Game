import random
import time

class WeedPlant:
    PLANT_MAX_HEIGHT = 300
    
    def __init__(self, strain):
        self.strain = strain
        self.height = 0
        self.water = 0
        self.light = 0
        self.nutrient = 0
        self.health = 100
        self.harvested = False
        self.trimmed = False

    def trim(self, trimming_time, trimming_effect):
        print(f"Trimming {self.strain['name']}... This will take {trimming_time} seconds.")
        time.sleep(trimming_time)
        # Apply the provided trimming effect
        trimming_effect(self)
        self.trimmed = True
        print("Trim applied.")

    def trim_light(self, trimming_time):
        # Light trimming increases branching and bushiness
        self.trim(trimming_time, lambda plant: self.trim_light_effect(plant))

    def trim_heavy(self, trimming_time):
        # Heavy trimming promotes taller growth with fewer branches
        self.trim(trimming_time, lambda plant: self.trim_heavy_effect(plant))

    def trim_selective(self, trimming_time):
        # Selective trimming focuses on specific branches, affecting overall shape
        self.trim(trimming_time, lambda plant: self.trim_selective_effect(plant))

    def trim_light_effect(self, plant):
        plant.height *= 0.7  # Reduce height
        plant.health -= random.randint(5, 10)  # Slightly decrease health

    def trim_heavy_effect(self, plant):
        plant.height *= 0.6  # Further reduce height
        plant.health -= random.randint(5, 15)  # Decrease health

    def trim_selective_effect(self, plant):
        plant.height *= 0.75  # Slightly reduce height
        plant.health += random.randint(1, 5)  # Slightly improve health

    def grow(self, light_factor, water_factor, nutrient_factor):
        self.water -= self.water * 0.03
        self.light -= self.light * 0.015
        self.nutrient -= self.nutrient * 0.03
        
        self.water += water_factor
        self.light += light_factor
        self.nutrient += nutrient_factor

        growth_factor = (self.light + self.water + self.nutrient) / 3

        if self.height >= self.PLANT_MAX_HEIGHT:
            self.health -= random.randint(15, 30)
            growth_factor -= growth_factor / 2

        if self.height >= self.PLANT_MAX_HEIGHT / 2:
            self.health -= random.randint(1, 10)
            growth_factor -= growth_factor / 5

        if self.water >= 12:
            self.health -= random.randint(5, 10)
            growth_factor -= growth_factor / 5

        if self.light >= 20:
            self.health -= random.randint(5, 15)
            growth_factor -= growth_factor / 4

        if self.nutrient >= 25:
            self.health -= random.randint(5, 25)
            growth_factor -= growth_factor / 3

        self.height += max(0, growth_factor)

        # Ensure values stay within a reasonable range
        self.water = max(0, min(60, self.water))
        self.light = max(0, min(60, self.light))
        self.nutrient = max(0, min(60, self.nutrient))

        if self.health <= 0:
            print("Your plant has withered away")
            return False
            
        return True

    def display_status(self):
        print(f"Plant Height: {self.height:.2f} cm")
        print(f"Plant Health: {self.health}%")

    def serialize(self):
        return {
            "strain": self.strain,
            "height": self.height,
            "water": self.water,
            "light": self.light,
            "nutrient": self.nutrient,
            "health": self.health,
            "harvested": self.harvested,
            "trimmed": self.trimmed
        }

    @classmethod
    def deserialize(cls, data):
        plant = cls(data["strain"])
        plant.height = data["height"]
        plant.water = data["water"]
        plant.light = data["light"]
        plant.nutrient = data["nutrient"]
        plant.health = data["health"]
        plant.harvested = data["harvested"]
        plant.trimmed = data["trimmed"]
        return plant
