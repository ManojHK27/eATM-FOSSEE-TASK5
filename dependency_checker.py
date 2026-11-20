"""Checks whether configured executables are available on PATH."""
import shutil
import subprocess

class DependencyChecker:
    def inspect(self, tool):
        executable = tool["executable"]
        path = shutil.which(executable)
        version = None
        if path:
            try:
                completed = subprocess.run(
                    [executable] + tool.get("version_args", ["--version"]),
                    capture_output=True, text=True, timeout=12, check=False
                )
                output = (completed.stdout or completed.stderr).strip()
                version = output.splitlines()[0][:180] if output else f"Available at {path}"
            except (OSError, subprocess.TimeoutExpired) as exc:
                version = f"Found, but version check failed: {exc}"
        return {"name": tool["name"], "installed": bool(path), "path": path, "version": version}

    def environment_report(self):
        import sys, platform
        import shutil as _shutil
        return [
            f"Operating system: {platform.platform()}",
            f"Python: {sys.version.split()[0]} ({sys.executable})",
            f"Git: {_shutil.which('git') or 'not found on PATH'}",
            f"winget: {_shutil.which('winget') or 'not found on PATH'}",
        ]
