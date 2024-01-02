"""
Wrapper commands for using docker containers and git
"""
import os
import pathlib
import subprocess
import typing as t


def _run_command(
    cmd: t.Union[str, t.Iterable[str]], cwd: t.Optional[pathlib.Path] = None
) -> int:
    if isinstance(cmd, str):
        cmd = cmd.split("")

    print(f"DEBUG: Running command '{' '.join(cmd)}' inside {cwd}")
    proc = subprocess.run(cmd, cwd=cwd)

    return proc.returncode


def run_vyos_build_cmd(
    cmd: t.Iterable[str],
    vyos_build_dir: pathlib.Path,
    vyos_release: str,
    sub_working_dir: str = None,
):
    docker_args = [
        "docker",
        "run",
        "--rm",
        "--sysctl",
        "net.ipv6.conf.lo.disable_ipv6=0",
        "--privileged",
        "-v",
        f"{vyos_build_dir.resolve()}:/vyos",
        "-w",
        f"/vyos/{sub_working_dir}",
        "-e",
        f"GOSU_UID={os.getuid()}",
        "-e",
        f"GOSU_GID={os.getgid()}",
        "-it",
        f"vyos/vyos-build:{vyos_release}",
    ]

    ret = _run_command(docker_args + cmd)
    if ret != 0:
        raise RuntimeError("Failure during vyos build command")


def clone_repo(url: str, branch: str, output_folder: pathlib.Path):
    git_args = [
        "git",
        "clone",
        url,
        "-b",
        branch,
        "--single-branch",
        str(output_folder),
    ]

    if output_folder.is_dir():
        print(f"WARN: {url} already cloned")
        return 0

    ret = _run_command(git_args)
    if ret != 0:
        raise RuntimeError("Failure during git clone command")


def apply_overlay(src: pathlib.Path, dst: pathlib.Path):
    # Add the trailing / to src to apply the subcontents as the overlay
    ret = _run_command(["rsync", "-a", f"{src}/", str(dst)])
    if ret != 0:
        raise RuntimeError("Failed to apply overlay")


def apply_patch(patch_path: pathlib.Path, dst: pathlib.Path):
    ret = _run_command(["git", "apply", str(patch_path.resolve())], cwd=dst)
    if ret != 0:
        raise RuntimeError("Failed to apply patch")
