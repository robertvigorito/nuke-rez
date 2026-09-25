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


def make_script(path, content):
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def test_wsl_launcher_sets_cmd_nuke_path_from_wsl_environment(tmp_path):
    module = load_package_module()
    mock_bin = tmp_path / "bin"
    capture_file = tmp_path / "cmd_capture.txt"
    mock_bin.mkdir()
    make_script(
        mock_bin / "wslpath",
        "#!/usr/bin/env bash\ninput=$2\nprintf 'C:%s\\n' \"${input//\\//\\\\}\"\n",
    )
    make_script(
        mock_bin / "cmd.exe",
        "#!/usr/bin/env bash\nprintf '%s' \"$2\" > \"$CMD_CAPTURE\"\n",
    )
    nk_file = tmp_path / "shot.nk"
    nk_file.write_text("", encoding="utf-8")
    command = module._wsl_launch_command(
        "/vfx/wgid/programs/Nuke15.1v1/Nuke15.1.exe", ("--nukex",)
    )
    env = os.environ | {
        "PATH": f"{mock_bin}:{os.environ.get('PATH', '')}",
        "CMD_CAPTURE": str(capture_file),
        "NUKE_PATH": "/mnt/c/tools:/show/shared/nuke",
    }

    result = subprocess.run(
        f"{command} {shlex.quote(str(nk_file))}", shell=True, env=env, check=False
    )

    expected_nk_path = f"C:{str(nk_file).replace('/', '\\')}"
    assert result.returncode == 0
    assert capture_file.read_text(encoding="utf-8") == (
        'set "NUKE_PATH=C:\\mnt\\c\\tools;C:\\show\\shared\\nuke" && '
        '"C:\\vfx\\wgid\\programs\\Nuke15.1v1\\Nuke15.1.exe" '
        f'"--nukex" "{expected_nk_path}"'
    )
