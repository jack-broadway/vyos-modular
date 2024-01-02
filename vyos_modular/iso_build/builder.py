import abc
import pathlib
import shutil
import typing as t

import vyos_modular.common.commands


class Builder(abc.ABC):
    def __init__(self, branch):
        self.branch = branch
        self.release = None
        self.slug = None

        # Setup the build folders
        self.build_dir = pathlib.Path("build")
        self.bin_dir = pathlib.Path("bin")
        self.vendor_dir = pathlib.Path("vendor")

        # Clear out the build directory as we dont want any artifacts left over
        shutil.rmtree(self.build_dir, ignore_errors=True)
        self.build_dir.mkdir(exist_ok=True)
        self.bin_dir.mkdir(exist_ok=True)
        self.vendor_dir.mkdir(exist_ok=True)

    def prepare(self):
        # Clone the selected vyos-build repository
        self.slug = f"vyos-build-{self.branch}-{self.release}"

        vyos_modular.common.commands.clone_repo(
            url="https://github.com/vyos/vyos-build.git",
            branch=self.branch,
            output_folder=self.vendor_dir / self.slug,
        )

        # Copy the vendor folder to build so we dont modify our copy. Symlinks is set to true because parts
        # of the build relies on symlinks being copied as symlinks for pathing related behavior
        shutil.copytree(
            self.vendor_dir / self.slug, self.build_dir / self.slug, symlinks=True
        )

    @abc.abstractmethod
    def build(self):
        raise NotImplementedError()


class EquuleusBuilder(Builder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.release = "equuleus"

    def build(self):
        self.prepare()

        configure_cmd = [
            "./configure",
            "--architecture",
            "amd64",
            "--build-type",
            "production",
            "--build-by",
            "jack-broadway/vyos-modular",
            "--version",
            self.branch,
        ]

        # Execute the configuration stage
        vyos_modular.common.commands.run_vyos_build_cmd(
            configure_cmd,
            vyos_build_dir=self.build_dir / self.slug,
            vyos_release=self.release,
        )

        # Execute the ISO build stage
        vyos_modular.common.commands.run_vyos_build_cmd(
            ["sudo", "make", "iso"],
            vyos_build_dir=self.build_dir / self.slug,
            vyos_release=self.release,
        )

        # Copy the resulting ISO to the bin folder
        build_output = self.build_dir / self.slug / "build"
        iso = next(build_output.glob("vyos-*.iso"))
        shutil.copy(iso, self.bin_dir)


class SagittaBuilder(Builder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.release = "sagitta"

    def build(self):
        self.prepare()

        # Sagitta has build and configure as one step
        build_cmd = [
            "sudo",
            "./build-vyos-image",
            "iso",
            "--architecture",
            "amd64",
            "--build-type",
            "release",
            "--build-by",
            "jack-broadway/vyos-modular",
            "--version",
            self.branch,
        ]

        vyos_modular.common.commands.run_vyos_build_cmd(
            build_cmd,
            vyos_build_dir=self.build_dir / self.slug,
            vyos_release=self.release,
        )

        # Copy the resulting ISO to the bin folder
        build_output = self.build_dir / self.slug / "build"
        iso = next(build_output.glob("vyos-*.iso"))
        shutil.copy(iso, self.bin_dir)


class CircinusBuilder(SagittaBuilder):
    # For now circinus hasnt diverged from the sagitta build process
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.release = "current"
