"""Checks winget update availability and asks before applying an update."""
import subprocess

class ToolUpdater:
    def __init__(self, logger):
        self.logger = logger

    def check_and_upgrade(self, tool):
        package_id = tool["winget_id"]
        check = ["winget", "upgrade", "--id", package_id, "--exact"]
        print("Checking:", " ".join(check))
        try:
            result = subprocess.run(check, text=True, capture_output=True, check=False)
            output = (result.stdout or "") + (result.stderr or "")
            print(output.strip() or f"winget returned exit code {result.returncode}.")
            if result.returncode != 0:
                self.logger.warning("Update check returned %s for %s", result.returncode, tool["name"])
            answer = input("If winget lists an update, apply it now? Type YES to continue: ")
            if answer != "YES":
                print("Update not started.")
                return
            command = ["winget", "upgrade", "--id", package_id, "--exact",
                       "--accept-package-agreements", "--accept-source-agreements"]
            self.logger.info("Starting update: %s", tool["name"])
            upgraded = subprocess.run(command, check=False)
            if upgraded.returncode == 0:
                print("winget upgrade command completed.")
                self.logger.info("Update command completed: %s", tool["name"])
            else:
                print(f"Update returned exit code {upgraded.returncode}.")
                self.logger.error("Update failed for %s; exit=%s", tool["name"], upgraded.returncode)
        except OSError as exc:
            print(f"Could not run winget: {exc}")
            self.logger.exception("Update operation failed for %s", tool["name"])
