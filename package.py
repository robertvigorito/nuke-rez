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
    """Build a WSL-safe launcher that converts paths with shell wslpath."""
    extra_args_definition = "extra_args=({})".format(
        " ".join(shlex.quote(arg) for arg in extra_args)
    )
    launcher = textwrap.dedent(
        """
        nuke_binary={nuke_binary}
        {extra_args_definition}

        convert_path() {{
            case "$1" in
                [A-Za-z]:[\\\\/]*)
                    printf '%s' "$1"
                    ;;
                *)
                    wslpath -w "$1" 2>/dev/null || printf '%s' "$1"
                    ;;
            esac
        }}

        escape_cmd_value() {{
            local value=$1
            value=${{value//^/^^}}
            value=${{value//%/%%}}
            value=${{value//&/^&}}
            value=${{value//|/^|}}
            value=${{value//</^<}}
            value=${{value//>/^>}}
            value=${{value//(/^(}}
            value=${{value//)/^)}}
            printf '%s' "$value"
        }}

        quote_cmd_arg() {{
            local value=$1
            value=${{value//%/%%}}
            printf '"%s"' "$value"
        }}

        split_nuke_path() {{
            if [[ -z "$1" ]]; then
                return
            fi

            if [[ "$1" == *";"* && "$1" =~ (^|;)[A-Za-z]:[\\\\/] ]]; then
                local old_ifs=$IFS
                IFS=';'
                read -r -a SPLIT_NUKE_PATH_RESULT <<< "$1"
                IFS=$old_ifs
            else
                local old_ifs=$IFS
                IFS=':'
                read -r -a SPLIT_NUKE_PATH_RESULT <<< "$1"
                IFS=$old_ifs
            fi
        }}

        convert_argument() {{
            if [[ -e "$1" ]]; then
                convert_path "$1"
                return
            fi

            if [[ "$1" == *=* ]]; then
                local option=${{1%%=*}}
                local value=${{1#*=}}
                if [[ -e "$value" ]]; then
                    printf '%s=%s' "$option" "$(convert_path "$value")"
                    return
                fi
            fi

            if [[ "$1" == *:* ]]; then
                local path_part=${{1%:*}}
                local suffix=${{1##*:}}
                if [[ "$suffix" =~ ^[0-9]+$ && -e "$path_part" ]]; then
                    printf '%s:%s' "$(convert_path "$path_part")" "$suffix"
                    return
                fi
            fi

            printf '%s' "$1"
        }}

        split_nuke_path "${{NUKE_PATH:-}}"
        converted_nuke_path=""
        for path_entry in "${{SPLIT_NUKE_PATH_RESULT[@]}}"; do
            [[ -z "$path_entry" ]] && continue
            converted_entry=$(convert_path "$path_entry")
            if [[ -n "$converted_nuke_path" ]]; then
                converted_nuke_path="$converted_nuke_path;$converted_entry"
            else
                converted_nuke_path=$converted_entry
            fi
        done

        command=$(quote_cmd_arg "$(convert_path "$nuke_binary")")
        for extra_arg in "${{extra_args[@]}}"; do
            command="$command $(quote_cmd_arg "$extra_arg")"
        done
        for cli_arg in "$@"; do
            command="$command $(quote_cmd_arg "$(convert_argument "$cli_arg")")"
        done

        if [[ -n "$converted_nuke_path" ]]; then
            command='set "NUKE_PATH='"$(escape_cmd_value "$converted_nuke_path")"'" && '"$command"
        fi

        cmd.exe /C "$command"
        """
    ).format(
        nuke_binary=shlex.quote(nuke_binary),
        extra_args_definition=extra_args_definition,
    )

    return "bash -lc {} --".format(shlex.quote(launcher))


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
