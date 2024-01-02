import argparse
import pathlib
import shutil

import vyos_modular.iso_build.builder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--branch", "-b", type=str, required=True, help="branch name or tag to build"
    )
    parser.add_argument(
        "--release",
        "-r",
        type=str,
        required=True,
        help="The release stream to build for (crux, equuleus, sagitta, current)",
    )

    args = parser.parse_args()

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


if __name__ == "__main__":
    main()
