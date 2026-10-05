"""The Nuke rez package, nothing special, just a wrapper around settings the environment to use Nuke in Rez."""

name = "nuke"
version = "15.1v1"
authors = ["Foundry"]
description = "Foundry Nuke compositing application"


build_command = False  # No build step


def commands():
    """Set up environment for Nuke.

    Returns:
        The fucntion does not return anything, it modifies the environment in place.
    """
    import os

    slim_version = "15.1v1"
    NUKE_ROOT = f"E:/wgid/bin/windows/Nuke{version}.lnk"
    nuke_binary = f"{NUKE_ROOT}/Nuke{slim_version}.exe"
    if os.environ.get("WSL_DISTRO_NAME"):
        alias("nuke", f"wsl-command  '{NUKE_ROOT}'")
        alias("nukex", f"wsl-command  '{NUKE_ROOT}' --nukex")
        alias("nukei", f"wsl-command  '{NUKE_ROOT}' --nukei")
    else:
        alias("nuke", nuke_binary)
        alias("nukex", f"{nuke_binary} --nukex")
        alias("nukei", f"{nuke_binary} --nukei")
