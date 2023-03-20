from typing import Optional
import urllib.request
import sys
import pathlib
import subprocess
import typing as t

from vyos_modular.model import PackageURL


def _run_command(
    cmd: t.Union[str, t.Iterable[str]], cwd: t.Optional[pathlib.Path] = None
) -> int:
    if isinstance(cmd, str):
        cmd = cmd.split(" ")

    print(f"DEBUG: Running command '{' '.join(cmd)}' inside {cwd}")
    proc = subprocess.run(cmd, cwd=cwd)

    return proc.returncode


def run_vyos_core_cmd(
    cmd: t.Iterable[str], vyos_core_dir: pathlib.Path, vyos_branch: str
):
    docker_args = [
        "docker",
        "run",
        "--rm",
        "--privileged",
        "--sysctl",
        "net.ipv6.conf.lo.disable_ipv6=0",
        "-v",
        f"{vyos_core_dir.resolve().parents[0]}:/vyos",
        "-w",
        "/vyos/vyos-core",
    ]

    if sys.stdout.isatty():
        docker_args.append("-it")

    docker_args.append(f"vyos/vyos-build:{vyos_branch}")

    ret = _run_command(docker_args + cmd, cwd=vyos_core_dir)
    if ret != 0:
        raise RuntimeError("Failure during vyos core command")


def run_vyos_build_cmd(
    cmd: t.Iterable[str], vyos_build_dir: pathlib.Path, vyos_branch: str
):

    docker_args = [
        "docker",
        "run",
        "--rm",
        "--privileged",
        "-v",
        f"{vyos_build_dir.resolve()}:/vyos",
        "-w",
        "/vyos",
    ]

    if sys.stdout.isatty():
        docker_args.append("-it")

    docker_args.append(f"vyos/vyos-build:{vyos_branch}")

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


def download_package(packages_dir: pathlib.Path, package_url: PackageURL):
    package_filename = package_url.filename
    if package_filename is None:
        package_filename = package_url.url.split("/")[-1]
        if not package_filename.endswith("deb"):
            raise RuntimeError("Cannot determine package filename after download")

    package_path = packages_dir / package_filename

    print(f"INFO: Downloading {package_url} to {package_path}")
    urllib.request.urlretrieve(package_url.url, package_path)
