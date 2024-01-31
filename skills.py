import os

class Skills:
    def __init__(self, level, xp):
        self.level = level
        self.xp = xp

    def add_xp(self, skill_name, xp_amount):
        # Ensure the skill_name is valid
        if skill_name not in self.level:
            print(f"Error: {skill_name} is not a valid skill/level.")
            return

        # Add XP to the specified skill/level
        self.xp[skill_name] += xp_amount

        # Check if the XP is enough to level up
        while self.xp[skill_name] >= self.calculate_xp_required(self.level[skill_name]):
            self.level_up(skill_name)

    def calculate_xp_required(self, current_level):
        # Define a simple formula for XP required for the next level
        return (current_level * 2) * 250

    def level_up(self, skill_name):
        # Increase the level and reset XP for the specified skill/level
        self.level[skill_name] += 1
        self.xp[skill_name] = 0
        print(f"{skill_name} leveled up to level {self.level[skill_name]}!")