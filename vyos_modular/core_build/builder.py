import os
import shutil
import typing as t

import vyos_modular.common.commands
from vyos_modular.common.config import GlobalConfig


class CoreBuilder:
    def __init__(self):
        self.config = GlobalConfig()

    def prepare(self):
        # Clone the selected vyos-build repository
        self.slug = f"vyos-core-{self.config.branch}-{self.config.release}"

        vyos_modular.common.commands.clone_repo(
            url="https://github.com/vyos/vyos-1x.git",
            branch=self.config.branch,
            output_folder=self.config.vendor_dir / self.slug,
        )

        # Copy the vendor folder to build so we dont modify our copy. Symlinks is set to true because parts
        # of the build relies on symlinks being copied as symlinks for pathing related behavior
        shutil.copytree(
            self.config.vendor_dir / self.slug,
            self.config.build_dir / self.slug,
            symlinks=True,
        )

    def apply(self):
        for module in self.config.modules:
            if not module.patches_core:
                continue

            print(f"INFO: Applying module {module.name}")
            vyos_core_overlay_path = (
                module.path / "vyos-core" / self.config.release / "overlay"
            )
            if vyos_core_overlay_path.is_dir():
                print(f"INFO: Applying vyos-core overlay from {module.name}")
                overlay_destination_path = self.config.build_dir / self.slug
                vyos_modular.common.commands.apply_overlay(
                    vyos_core_overlay_path, overlay_destination_path
                )
            vyos_core_patch_path = (
                module.path / "vyos-core" / self.config.release / "patches"
            )
            if vyos_core_patch_path.is_dir():
                for patch in vyos_core_patch_path.iterdir():
                    print(
                        f"INFO: Applying patch {patch.name} from {module.name} to vyos-core"
                    )
                    vyos_modular.common.commands.apply_patch(
                        patch, self.config.build_dir / self.slug
                    )

    def build(self):
        self.prepare()
        self.apply()
        # Build vyos-core. Because dpkg will drop the built deb one level up,
        # have to mount the build directory and set the working directory one level lower
        vyos_modular.common.commands.run_vyos_build_cmd(
            [
                "dpkg-buildpackage",
                "-uc",
                "-us",
                "-tc",
                "-b",
            ],
            vyos_build_dir=self.config.build_dir,
            sub_working_dir=self.slug,
            vyos_release=self.config.release,
        )

        # Copy out all the debs for vyos core including testing etc to bin folder. User may want to test
        for deb in self.config.build_dir.glob("*.deb"):
            shutil.copy(deb, self.config.bin_dir)

        # Remove any existing core deb from the resources folder and copy the freshly built one over
        for deb in self.config.resource_dir.glob("*.deb"):
            os.remove(deb)
        iso_deb = next(self.config.build_dir.glob("vyos-1x_*.deb"))
        shutil.copy(iso_deb, self.config.resource_dir)
