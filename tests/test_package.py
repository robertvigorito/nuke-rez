import importlib.util
import os
import shlex
import subprocess
from pathlib import Path


def load_package_module():
    package_path = Path(__file__).resolve().parents[1] / "package.py"
    spec = importlib.util.spec_from_file_location("nuke_package", package_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_wsl_launcher_sets_cmd_nuke_path_from_wsl_environment(tmp_path):
    module = load_package_module()

    capture_file = tmp_path / "cmd_capture.txt"
    mock_bin = tmp_path / "bin"
    mock_bin.mkdir()

    wslpath_script = mock_bin / "wslpath"
    wslpath_script.write_text(
        "#!/usr/bin/env bash\n"
        "input=$2\n"
        "printf 'C:%s\\n' \"${input//\\//\\\\}\"\n",
        encoding="utf-8",
    )
    wslpath_script.chmod(0o755)

    cmd_script = mock_bin / "cmd.exe"
    cmd_script.write_text(
        "#!/usr/bin/env bash\n"
        "printf '%s' \"$2\" > \"$CMD_CAPTURE\"\n",
        encoding="utf-8",
    )
    cmd_script.chmod(0o755)

    nk_file = tmp_path / "shot.nk"
    nk_file.write_text("", encoding="utf-8")

    command = module._wsl_launch_command(
        "/vfx/wgid/programs/Nuke15.1v1/Nuke15.1.exe",
        ("--nukex",),
    )
    command = "{} {}".format(command, shlex.quote(str(nk_file)))

    env = os.environ.copy()
    env["PATH"] = "{}:{}".format(mock_bin, env.get("PATH", ""))
    env["CMD_CAPTURE"] = str(capture_file)
    env["NUKE_PATH"] = "/mnt/c/tools:/show/shared/nuke"

    result = subprocess.run(command, shell=True, env=env, check=False)

    assert result.returncode == 0
    assert capture_file.read_text(encoding="utf-8") == (
        'set "NUKE_PATH=C:\\mnt\\c\\tools;C:\\show\\shared\\nuke" && '
        '"C:\\vfx\\wgid\\programs\\Nuke15.1v1\\Nuke15.1.exe" '
        '"--nukex" '
        '"{}"'.format(str(nk_file).replace("/", "\\"))
    )
