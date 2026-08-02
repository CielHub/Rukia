"""
main.py
CARRERA-HUB v2
Core Entry Point
"""

from menu import Menu
from package_manager import PackageManager
from private_server_manager import PrivateServerManager
from launcher import Launcher
from verification_engine import VerificationEngine
from monitor_engine import MonitorEngine
from error_detection_engine import ErrorDetectionEngine
from recovery_engine import RecoveryEngine
from dashboard import Dashboard


class CarreraHub:

    def __init__(self):
        self.menu = Menu()
        self.package_manager = PackageManager()
        self.private_server = PrivateServerManager()
        self.launcher = Launcher()
        self.verifier = VerificationEngine()
        self.monitor = MonitorEngine()
        self.error_detector = ErrorDetectionEngine()
        self.recovery = RecoveryEngine(
            launcher=self.launcher,
            verifier=self.verifier,
        )
        self.dashboard = Dashboard()

    def start_runtime(self):
        packages = self.package_manager.load()

        if not packages:
            print("No package selected.")
            return

        self.launcher.start()

        self.monitor.set_packages(packages)
        self.monitor.set_callback(self.recovery.handle_monitor_event)
        self.monitor.start()

        print("Runtime started.")

    def stop_runtime(self):
        self.monitor.stop()
        self.monitor.join()
        print("Runtime stopped.")

    def run(self):
        while True:
            self.menu.clear()
            self.menu.header()
            choice = self.menu.prompt()

            if choice == "1":
                self.package_manager.scan()
                self.package_manager.display()
                self.package_manager.select()

            elif choice == "2":
                link = input("Private Server Link: ").strip()
                self.private_server.save(link)

            elif choice == "3":
                selected = self.package_manager.load()
                data = [
                    {"package": p, "status": "READY", "error": "-"}
                    for p in selected
                ]
                self.dashboard.render(data)
                input("\nPress ENTER...")

            elif choice == "4":
                self.start_runtime()
                input("\nPress ENTER...")

            elif choice == "5":
                self.stop_runtime()
                input("\nPress ENTER...")

            elif choice == "6":
                print("Settings coming soon.")
                input("\nPress ENTER...")

            elif choice == "7":
                self.stop_runtime()
                break


if __name__ == "__main__":
    CarreraHub().run()
  
