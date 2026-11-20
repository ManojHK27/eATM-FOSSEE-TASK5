"""Command-line interface and orchestration for eATM."""
from pathlib import Path
import json
from dependency_checker import DependencyChecker
from installer import ToolInstaller
from updater import ToolUpdater
from logger_setup import get_logger

ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "config" / "tools.json"
logger = get_logger(ROOT / "logs" / "eatm.log")

class ToolManager:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = Path(config_file)
        self.tools = json.loads(self.config_file.read_text(encoding="utf-8"))["tools"]
        self.checker = DependencyChecker()
        self.installer = ToolInstaller(logger)
        self.updater = ToolUpdater(logger)

    def show_tools(self):
        print("\nConfigured tools")
        print("-" * 72)
        for tool in self.tools:
            result = self.checker.inspect(tool)
            status = "INSTALLED" if result["installed"] else "NOT FOUND"
            version = result["version"] or "-"
            print(f'{tool["name"]:<18} {status:<12} {version}')
        print("-" * 72)

    def install_tool(self):
        self.show_tools()
        name = input("Enter the exact tool name to install: ").strip().lower()
        tool = next((t for t in self.tools if t["name"].lower() == name), None)
        if not tool:
            print("Tool not found in config/tools.json.")
            return
        if not tool.get("winget_id"):
            print("No winget package ID configured for this tool.")
            return
        if not self.installer.winget_available():
            print("winget is not available. Install/enable Windows App Installer first.")
            return
        confirm = input(f'Install {tool["name"]} using winget? Type YES to continue: ')
        if confirm != "YES":
            print("Installation cancelled.")
            return
        self.installer.install(tool)

    def update_tool(self):
        self.show_tools()
        name = input("Enter the exact tool name to update: ").strip().lower()
        tool = next((t for t in self.tools if t["name"].lower() == name), None)
        if not tool:
            print("Tool not found in config/tools.json.")
            return
        if not tool.get("winget_id"):
            print("No winget package ID configured for this tool.")
            return
        if not self.installer.winget_available():
            print("winget is not available.")
            return
        self.updater.check_and_upgrade(tool)

    def run(self):
        while True:
            print("\n=== eATM: eSim Automated Tool Manager ===")
            print("1. Check configured tools and versions")
            print("2. Install a tool (winget)")
            print("3. Check and apply an update (winget)")
            print("4. Show dependency/environment checks")
            print("5. Exit")
            choice = input("Choose an option [1-5]: ").strip()
            if choice == "1":
                self.show_tools()
            elif choice == "2":
                self.install_tool()
            elif choice == "3":
                self.update_tool()
            elif choice == "4":
                for item in self.checker.environment_report():
                    print(item)
            elif choice == "5":
                print("Exiting eATM.")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 5.")

if __name__ == "__main__":
    ToolManager().run()
