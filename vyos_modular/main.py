import argparse
import importlib.metadata
import pathlib
import shutil

import yaml

import vyos_modular.iso_build.builder
from vyos_modular.common.config import GlobalConfig
from vyos_modular.core_build.builder import CoreBuilder
from vyos_modular.iso_customize.builder import CustomBuilder


def _iso_build(args):
    builder: vyos_modular.iso_build.builder.Builder = None
    match args.release:
        case "equuleus":
            builder = vyos_modular.iso_build.builder.EquuleusBuilder(args.branch)
        case "sagitta":
            builder = vyos_modular.iso_build.builder.SagittaBuilder(args.branch)
        case "current" | "circinus":
            # While the release is codenamed circinus,
            # as it is the in dev branch its branch name is current
            args.branch = "current"
            builder = vyos_modular.iso_build.builder.CircinusBuilder(args.branch)
        case _:
            raise ValueError("Unsupported release stream to build for")
    builder.build()


def _build(args):
    with open(args.config) as config_fh:
        modular_config = yaml.load(config_fh, Loader=yaml.SafeLoader)

    config = GlobalConfig()
    config.config = modular_config

    patches_core = any([module.patches_core for module in config.modules])
    if patches_core:
        print("There are modules that patch vyos-core, building now")
        builder = CoreBuilder()
        builder.build()

    custom_builder = CustomBuilder()
    custom_builder.build()


def _init(_):
    dist_folder = pathlib.Path("dist")

    isos_folder = dist_folder / "isos"
    packages_folder = dist_folder / "packages"

    dist_folder.mkdir(exist_ok=True)
    isos_folder.mkdir(exist_ok=True)
    packages_folder.mkdir(exist_ok=True)

    with importlib.resources.path(
        "vyos_modular.templates", "sample_config.yml"
    ) as sample_config_path:
        shutil.copy(sample_config_path, "config.yml")


def run(args):
    match args.command:
        case "build_iso":
            _iso_build(args)
        case "build":
            _build(args)
        case "init":
            _init(args)
        case _:
            raise RuntimeError(f"Unsupported command: {args.command}")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    # build_iso subcommand so you can build clean ISOs to be later used for customizing
    iso_parser = subparsers.add_parser("build_iso")
    iso_parser.add_argument(
        "--branch", "-b", type=str, required=True, help="branch name or tag to build"
    )
    iso_parser.add_argument(
        "--release",
        "-r",
        type=str,
        required=True,
        help="The release stream to build for (crux, equuleus, sagitta, current)",
    )

    core_parser = subparsers.add_parser("build")
    core_parser.add_argument("--config", "-c", type=pathlib.Path, required=True)

    subparsers.add_parser("init")

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
