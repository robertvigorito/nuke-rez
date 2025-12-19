"""The Nuke rez package, nothing special, just a wrapper around settings the environment to use Nuke in Rez."""

name = "nuke"
version = "16.0v1"

authors = ["Foundry"]
description = "Foundry Nuke compositing application"

# requires = ["python-3.9"]

build_command = False  # No build step


def commands():
    # Root install path
    NUKE_ROOT = f"/vfx/wgid/programs/Nuke{version}"

    # Main binaries
    env.PATH.prepend("{NUKE_ROOT}")

    # Libraries
    env.LD_LIBRARY_PATH.prepend("{NUKE_ROOT}/lib")

    # Nuke-specific paths
    env.NUKE_PATH.append("{NUKE_ROOT}/plugins")
    env.NUKE_PATH.append("{NUKE_ROOT}/gizmos")

    # Optional: site-wide config
    env.NUKE_PATH.append("/studio/nuke/plugins")
    env.NUKE_PATH.append("/studio/nuke/gizmos")

    slim_version = version.split("v")[0]
    # Convenience aliases
    alias("nuke", f"{NUKE_ROOT}/Nuke{slim_version}.exe")
    alias("nukex", f"{NUKE_ROOT}/Nuke{slim_version}.exe --nukex")
    alias("nukei", f"{NUKE_ROOT}/Nuke{slim_version}.exe --nukei")
