# eATM — eSim Automated Tool Manager

A Python command-line proof of concept for managing external tools used in an eSim-style EDA workflow on Windows.

## Features implemented
1. **Tool installation management:** invokes Windows Package Manager (`winget`) for configured packages after explicit user confirmation.
2. **Dependency checker:** detects configured executables on `PATH` and captures their version output.
3. **Update management:** checks `winget upgrade` and asks before running an upgrade.
4. **Configuration and logs:** tool metadata is stored in `config/tools.json`; actions/errors are written to `logs/eatm.log`.
5. **Environment report:** displays OS, Python, Git and winget availability.

## Requirements
- Windows 10/11
- Python 3.10 or later (standard library only)
- Windows Package Manager (App Installer) for install/update functions
- Internet access for winget package operations

## Run
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py main.py
```
If PowerShell blocks activation, run without activating:
```powershell
.\.venv\Scripts\python.exe main.py
```

## Test
```powershell
py -m unittest discover -s tests -v
```

## Configure tools
Edit `config/tools.json`. Each entry requires:
- `name`: display name
- `executable`: command checked on PATH
- `version_args`: arguments used to print the version
- `winget_id`: exact package ID used for install/update

Verify package IDs and availability with `winget search <name>` before using installation. The default Python package ID is an example pinned to Python 3.13; change it if you need another version.

## Safety
- Installation and upgrades change the computer. The program requires the user to type `YES` before starting either operation.
- Review package identity and publisher in winget before confirming.
- The program does not run with administrator privileges automatically.
- A tool may be installed but not detected if its executable is not on PATH. Restart the terminal after changing PATH.
- Package IDs and command-line version switches can change. Verify them on the target computer.

## Limitations
- This is a prototype, not an official eSim installer and not a guarantee of compatibility with every eSim release.
- Windows package installation depends on winget, package availability, network access and local permissions.
- Update output is displayed for user review; the tool does not silently upgrade packages.
- Linux/macOS support is not implemented in this version.

## Project layout
See `docs/DESIGN_DOCUMENT.md` for architecture and `docs/TEST_PLAN.md` for validation steps.
