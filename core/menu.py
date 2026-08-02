"""
menu.py
CARRERA-HUB v2
Core Menu
"""

from __future__ import annotations
import os

class Menu:
    def __init__(self):
        self.running=True

    def clear(self):
        os.system("clear")

    def header(self):
        print("╔══════════════════════════════════════════════════════╗")
        print("║                  RUKIA HUB                                     ║")
        print("╠══════════════════════════════════════════════════════╣")
        print("║ 1. Package Manager                                             ║")
        print("║ 2. Private Server Manager                                      ║")
        print("║ 3. Dashboard                                                   ║")
        print("║ 4. Start Auto Rejoin                                           ║")
        print("║ 5. Stop Runtime                                                ║")
        print("║ 6. Settings                                                    ║")
        print("║ 7. Exit                                                        ║")
        print("╚══════════════════════════════════════════════════════╝")

    def prompt(self):
        return input("\nSelect Menu > ").strip()

    def dispatch(self, choice):
        return {
            "1":"package_manager",
            "2":"private_server_manager",
            "3":"dashboard",
            "4":"start_runtime",
            "5":"stop_runtime",
            "6":"settings",
            "7":"exit",
        }.get(choice)

    def run(self):
        while self.running:
            self.clear()
            self.header()
            action=self.dispatch(self.prompt())

            if action=="exit":
                print("\nGoodbye.")
                break

            if action:
                print(f"\n[TODO] {action}")
            else:
                print("\nInvalid menu.")

            input("\nPress ENTER to continue...")

if __name__=="__main__":
    Menu().run()
  
