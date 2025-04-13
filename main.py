import sys
import time
import pickle
from os import path

class AdventureGame:
    def __init__(self):
        self.player_name = ""
        self.inventory = []
        self.health = 100
        self.current_room = "start"
        self.game_over = False
        self.visited_rooms = set()
        self.game_state_file = "adventure_save.pkl"

    def clear_screen(self):
        """Clear the console screen"""
        print("\n" * 100)

    def type_text(self, text, delay=0.03):
        """Print text with a typewriter effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def show_title(self):
        """Display the game title"""
        self.clear_screen()
        print("====================================")
        print("       PYTHON TEXT ADVENTURE        ")
        print("====================================")
        print()

    def get_player_name(self):
        """Get the player's name"""
        self.type_text("Welcome, adventurer!")
        self.type_text("What is your name?")
        self.player_name = input("> ").strip()
        while not self.player_name:
            self.type_text("Please enter your name:")
            self.player_name = input("> ").strip()

    def show_status(self):
        """Display player status"""
        print("\n" + "="*40)
        print(f"Name: {self.player_name}")
        print(f"Health: {self.health}")
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print(f"Location: {self.current_room.replace('_', ' ').title()}")
        print("="*40 + "\n")

    def handle_choice(self, prompt, options):
        """Handle player choices with validation"""
        while True:
            self.type_text(prompt)
            for i, option in enumerate(options, 1):
                self.type_text(f"{i}. {option}")

            choice = input("> ").strip().lower()

            # Check for numeric choice
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice)-1]

            # Check for text choice (first word)
            for option in options:
                if option.lower().startswith(choice):
                    return option

            self.type_text("Invalid choice. Please try again.")

    def add_to_inventory(self, item):
        """Add an item to the player's inventory"""
        if item not in self.inventory:
            self.inventory.append(item)
            self.type_text(f"You picked up: {item}")

    def remove_from_inventory(self, item):
        """Remove an item from the player's inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
            self.type_text(f"You used: {item}")

    def take_damage(self, amount):
        """Reduce player health"""
        self.health -= amount
        if self.health <= 0:
            self.type_text("You have died! Game over.")
            self.game_over = True
        else:
            self.type_text(f"You took {amount} damage! Health is now {self.health}.")

    def heal(self, amount):
        """Restore player health"""
        self.health = min(100, self.health + amount)
        self.type_text(f"You healed {amount} points. Health is now {self.health}.")

    def save_game(self):
        """Save the current game state"""
        with open(self.game_state_file, 'wb') as f:
            pickle.dump({
                'player_name': self.player_name,
                'inventory': self.inventory,
                'health': self.health,
                'current_room': self.current_room,
                'visited_rooms': self.visited_rooms
            }, f)
        self.type_text("Game saved successfully!")

    def load_game(self):
        """Load a saved game state"""
        if not path.exists(self.game_state_file):
            self.type_text("No saved game found.")
            return False

        try:
            with open(self.game_state_file, 'rb') as f:
                data = pickle.load(f)
                self.player_name = data['player_name']
                self.inventory = data['inventory']
                self.health = data['health']
                self.current_room = data['current_room']
                self.visited_rooms = data['visited_rooms']
            self.type_text("Game loaded successfully!")
            return True
        except:
            self.type_text("Failed to load saved game.")
            return False

    def start_room(self):
        """The starting room of the game"""
        self.current_room = "start"
        self.visited_rooms.add(self.current_room)

        if len(self.visited_rooms) == 1:
            self.type_text("You wake up in a dimly lit room with no memory of how you got here.")
            self.type_text("The air is damp and cold. You can hear distant dripping water.")
        else:
            self.type_text("You return to the room where you first woke up.")

        self.type_text("\nThere are two doors: one to your LEFT and one to your RIGHT.")
        self.type_text("There's also a small CHEST in the corner.")

        choice = self.handle_choice("What will you do?", [
            "Go left",
            "Go right",
            "Open chest",
            "Check inventory",
            "Save game",
            "Quit game"
        ])

        if choice == "Go left":
            self.corridor_room()
        elif choice == "Go right":
            self.kitchen_room()
        elif choice == "Open chest":
            if "key" not in self.inventory:
                self.type_text("You open the chest and find a rusty KEY inside.")
                self.add_to_inventory("key")
            else:
                self.type_text("The chest is empty.")
        elif choice == "Check inventory":
            self.show_status()
            self.start_room()
        elif choice == "Save game":
            self.save_game()
            self.start_room()
        elif choice == "Quit game":
            self.game_over = True

    def corridor_room(self):
        """The corridor room"""
        self.current_room = "corridor"
        self.visited_rooms.add(self.current_room)

        if self.current_room not in self.visited_rooms:
            self.type_text("You enter a long, dark corridor. The floor creaks with each step.")
        else:
            self.type_text("You're back in the creaky corridor.")

        self.type_text("\nAt the end of the corridor is a heavy DOOR with a keyhole.")
        self.type_text("You can also go BACK to the previous room.")

        choice = self.handle_choice("What will you do?", [
            "Try door",
            "Go back",
            "Check inventory"
        ])

        if choice == "Try door":
            if "key" in self.inventory:
                self.type_text("The key fits! The door unlocks with a satisfying click.")
                self.remove_from_inventory("key")
                self.treasure_room()
            else:
                self.type_text("The door is locked. You need a key to open it.")
                self.corridor_room()
        elif choice == "Go back":
            self.start_room()
        elif choice == "Check inventory":
            self.show_status()
            self.corridor_room()

    def kitchen_room(self):
        """The kitchen room"""
        self.current_room = "kitchen"
        self.visited_rooms.add(self.current_room)

        if self.current_room not in self.visited_rooms:
            self.type_text("You enter what appears to be an abandoned kitchen.")
            self.type_text("There's a foul smell coming from the pantry.")
        else:
            self.type_text("You're back in the smelly kitchen.")

        self.type_text("\nYou see a KNIFE on the counter and the PANTRY door is slightly ajar.")
        self.type_text("You can also go BACK to the previous room.")

        choice = self.handle_choice("What will you do?", [
            "Take knife",
            "Open pantry",
            "Go back",
            "Check inventory"
        ])

        if choice == "Take knife":
            if "knife" not in self.inventory:
                self.add_to_inventory("knife")
                self.type_text("You take the knife. It might be useful for protection.")
            else:
                self.type_text("You already have the knife.")
            self.kitchen_room()
        elif choice == "Open pantry":
            self.pantry_room()
        elif choice == "Go back":
            self.start_room()
        elif choice == "Check inventory":
            self.show_status()
            self.kitchen_room()

    def pantry_room(self):
        """The pantry room with a monster"""
        self.current_room = "pantry"
        self.visited_rooms.add(self.current_room)

        if self.current_room not in self.visited_rooms:
            self.type_text("As you open the pantry door, a horrible stench overwhelms you!")
            self.type_text("A grotesque creature leaps at you from the shadows!")

            if "knife" in self.inventory:
                self.type_text("You quickly pull out your knife and defend yourself!")
                self.type_text("The creature lets out a shriek and retreats into the darkness.")
                self.type_text("In the commotion, you notice a small MEDALLION on the floor.")

                choice = self.handle_choice("What will you do?", [
                    "Take medallion",
                    "Go back"
                ])

                if choice == "Take medallion":
                    self.add_to_inventory("medallion")
                    self.type_text("The medallion feels warm to the touch.")
                    self.kitchen_room()
                else:
                    self.kitchen_room()
            else:
                self.take_damage(50)
                if not self.game_over:
                    self.type_text("You manage to escape back to the kitchen, badly wounded.")
                    self.kitchen_room()
        else:
            self.type_text("The pantry is empty now, except for the lingering smell.")
            self.type_text("You can go BACK to the kitchen.")

            choice = self.handle_choice("What will you do?", ["Go back"])
            self.kitchen_room()

    def treasure_room(self):
        """The treasure room (final room)"""
        self.current_room = "treasure_room"
        self.visited_rooms.add(self.current_room)

        self.type_text("You enter a magnificent chamber filled with gold and jewels!")

        if "medallion" in self.inventory:
            self.type_text("The medallion in your pocket begins to glow brightly!")
            self.type_text("A portal opens before you, offering escape from this place!")

            choice = self.handle_choice("What will you do?", [
                "Enter portal",
                "Take treasure",
                "Go back"
            ])

            if choice == "Enter portal":
                self.type_text("As you step through the portal, you feel a warm light surround you.")
                self.type_text("You find yourself back in your own home, safe and sound.")
                self.type_text("Congratulations! You've escaped with your life and the mysterious medallion!")
                self.game_over = True
            elif choice == "Take treasure":
                self.type_text("Greed overwhelms you as you stuff your pockets with gold.")
                self.type_text("Suddenly, the door slams shut and the ceiling begins to lower!")
                self.type_text("You've triggered a trap! There's no escape!")
                self.game_over = True
            else:
                self.corridor_room()
        else:
            self.type_text("As you admire the treasure, you hear the door lock behind you!")
            self.type_text("You're trapped in the treasure room forever!")
            self.game_over = True

    def main_menu(self):
        """Show the main menu"""
        self.show_title()
        self.type_text("1. New Game")
        self.type_text("2. Load Game")
        self.type_text("3. Quit")

        choice = input("> ").strip()

        if choice == "1":
            self.get_player_name()
            self.start_room()
        elif choice == "2":
            if self.load_game():
                self.start_room()
            else:
                self.main_menu()
        elif choice == "3":
            self.game_over = True
        else:
            self.type_text("Invalid choice. Please try again.")
            self.main_menu()

    def play(self):
        """Main game loop"""
        while not self.game_over:
            if not self.player_name:
                self.main_menu()
            else:
                if self.current_room == "start":
                    self.start_room()
                elif self.current_room == "corridor":
                    self.corridor_room()
                elif self.current_room == "kitchen":
                    self.kitchen_room()
                elif self.current_room == "pantry":
                    self.pantry_room()
                elif self.current_room == "treasure_room":
                    self.treasure_room()

        self.type_text("Thanks for playing!")
        time.sleep(2)

# Start the game
if __name__ == "__main__":
    game = AdventureGame()
    game.play()
