"""The Nuke rez package, nothing special, just a wrapper around settings the environment to use Nuke in Rez."""

name = "nuke"
version = "16.0v1"
authors = ["Foundry"]
description = "Foundry Nuke compositing application"

# requires = ["python-3.9"]

build_command = False  # No build step


def commands():
    """Set up environment for Nuke.

    Returns:
        The fucntion does not return anything, it modifies the environment in place.
    """
    slim_version = "16.0"
    NUKE_ROOT = f"/vfx/wgid/programs/Nuke{version}"

    # Convenience aliases
    alias("nuke", f"{NUKE_ROOT}/Nuke{slim_version}.exe")
    alias("nukex", f"{NUKE_ROOT}/Nuke{slim_version}.exe --nukex")
    alias("nukei", f"{NUKE_ROOT}/Nuke{slim_version}.exe --nukei")
