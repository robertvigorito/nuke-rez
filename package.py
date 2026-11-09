"""The Nuke rez package, nothing special, just a wrapper around settings the environment to use Nuke in Rez."""

name = "nuke"
version = "17.1v3"
authors = ["Foundry"]
description = "Foundry Nuke compositing application"

# requires = ["python-3.9"]

build_command = False  # No build step


def commands():
    """Set up environment for Nuke.

    Returns:
        The fucntion does not return anything, it modifies the environment in place.
    """

    # Set the passover for WSL environment variables when loading nuke environment
    env.WSLENV.append("PYTHONPATH/lpw:NUKE_PATH/lpw")

    slim_version = "17.1"
    nuke_executable = f"/vfx/wgid/programs/Nuke{version}/Nuke{slim_version}.exe"

    alias("nuke", f"{nuke_executable} --nukex")
    alias("nukestudio", f"{nuke_executable} --nc --studio")
    alias("nukex", f"{nuke_executable} --nukex")
