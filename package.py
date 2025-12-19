"""The Nuke rez package, nothing special, just a wrapper around settings the environment to use Nuke in Rez."""

name = "nuke"
version = "16.0v1"

authors = ["Foundry"]
description = "Foundry Nuke compositing application"

requires = ["python-3.9"]

variants = [["platform-linux"]]


def commands():
    # Root install path
    env.NUKE_ROOT = f"/vfx/wgid/programs/Nuke{version}"

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

    # Convenience aliases
    alias("nuke", "{NUKE_ROOT}/Nuke14.0")
    alias("nukex", "{NUKE_ROOT}/Nuke14.0 --nukex")
    alias("nukei", "{NUKE_ROOT}/Nuke14.0 --nukei")
