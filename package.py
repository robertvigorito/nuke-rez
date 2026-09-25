"""The Nuke rez package, nothing special, just a wrapper around settings the environment to use Nuke in Rez."""

import os
import shlex
import textwrap

name = "nuke"
version = "15.1v1"
authors = ["Foundry"]
description = "Foundry Nuke compositing application"

# requires = ["python-3.9"]

build_command = False  # No build step


def _is_wsl():
    """Return True when running inside WSL."""
    if os.environ.get("WSL_DISTRO_NAME"):
        return True

    try:
        with open("/proc/version", encoding="utf-8") as version_file:
            return "microsoft" in version_file.read().lower()
    except OSError:
        return False


def _wsl_launch_command(nuke_binary, extra_args=()):
    """Build a WSL-safe launcher that converts NUKE_PATH for cmd.exe."""
    launcher = textwrap.dedent(
        """
        import os
        import re
        import subprocess
        import sys

        def convert_path(path):
            try:
                return subprocess.check_output(["wslpath", "-w", path], text=True).strip()
            except (OSError, subprocess.CalledProcessError):
                return path

        def escape_cmd_value(value):
            value = value.replace("^", "^^").replace("%", "%%")
            for character in "&|<>()":
                value = value.replace(character, "^" + character)
            return value

        def split_nuke_path(value):
            if not value:
                return []
            if ";" in value and re.search(r"(?:^|;)[A-Za-z]:[\\\\/]", value):
                return [path for path in value.split(";") if path]
            return [path for path in value.split(os.pathsep) if path]

        def convert_argument(argument):
            if os.path.exists(argument):
                return convert_path(argument)
            return argument

        nuke_binary = {nuke_binary!r}
        extra_args = {extra_args!r}
        nuke_path = ";".join(
            convert_path(path)
            for path in split_nuke_path(os.environ.get("NUKE_PATH", ""))
        )

        command = subprocess.list2cmdline(
            [convert_path(nuke_binary)]
            + list(extra_args)
            + [convert_argument(argument) for argument in sys.argv[1:]]
        )
        if nuke_path:
            command = 'set "NUKE_PATH=' + escape_cmd_value(nuke_path) + '" && ' + command

        sys.exit(subprocess.run(["cmd.exe", "/C", command]).returncode)
        """
    ).format(nuke_binary=nuke_binary, extra_args=extra_args)

    return "python -c {}".format(shlex.quote(launcher))


def commands():
    """Set up environment for Nuke.

    Returns:
        The fucntion does not return anything, it modifies the environment in place.
    """
    slim_version = "15.1"
    NUKE_ROOT = f"/vfx/wgid/programs/Nuke{version}"

    nuke_binary = f"{NUKE_ROOT}/Nuke{slim_version}.exe"

    if _is_wsl():
        alias("nuke", _wsl_launch_command(nuke_binary))
        alias("nukex", _wsl_launch_command(nuke_binary, ("--nukex",)))
        alias("nukei", _wsl_launch_command(nuke_binary, ("--nukei",)))
    else:
        alias("nuke", nuke_binary)
        alias("nukex", f"{nuke_binary} --nukex")
        alias("nukei", f"{nuke_binary} --nukei")
