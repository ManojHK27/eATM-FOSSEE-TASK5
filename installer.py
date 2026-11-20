"""Explicit, user-confirmed Windows installation via winget."""
import shutil
import subprocess

class ToolInstaller:
    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def winget_available():
        return shutil.which("winget") is not None

    def install(self, tool):
        package_id = tool["winget_id"]
        command = [
            "winget", "install", "--id", package_id, "--exact",
            "--accept-package-agreements", "--accept-source-agreements"
        ]
        print("Running:", " ".join(command))
        self.logger.info("Starting install: %s (%s)", tool["name"], package_id)
        try:
            result = subprocess.run(command, text=True, check=False)
            if result.returncode == 0:
                print("winget reported successful installation.")
                self.logger.info("Install completed: %s", tool["name"])
            else:
                print(f"Installation returned exit code {result.returncode}. Review winget output.")
                self.logger.error("Install failed for %s; exit=%s", tool["name"], result.returncode)
        except OSError as exc:
            print(f"Could not start winget: {exc}")
            self.logger.exception("Could not start winget for %s", tool["name"])
