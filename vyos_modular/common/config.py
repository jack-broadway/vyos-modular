import dataclasses
import pathlib
import shutil
import typing as t

import yaml

import vyos_modular.common.commands


@dataclasses.dataclass
class VyosModule:
    name: str
    path: pathlib.Path
    patches_core: bool
    config: t.Dict


class GlobalConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalConfig, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Setup the build folders
        self.build_dir = pathlib.Path("build")
        self.bin_dir = pathlib.Path("bin")
        self.vendor_dir = pathlib.Path("vendor")
        self.resource_dir = pathlib.Path("resources")

        # Clear out the build directory as we dont want any artifacts left over
        shutil.rmtree(self.build_dir, ignore_errors=True)
        self.build_dir.mkdir(exist_ok=True)
        self.bin_dir.mkdir(exist_ok=True)
        self.vendor_dir.mkdir(exist_ok=True)
        self.resource_dir.mkdir(exist_ok=True)

    def _process_config(self):
        self._branch = self._raw_config["vyos_target"]["branch"]
        self._release = self._raw_config["vyos_target"]["release"]
        self._modules: t.List[VyosModule] = []

        if "modules" not in self._raw_config or not self._raw_config["modules"]:
            raise RuntimeError("Must define at least one module in your configuration")

        for module in self._raw_config["modules"]:
            # Clone / Copy module to vendor folder
            module_dest = None
            if module["type"] == "local":
                path = pathlib.Path(module["path"])
                module_slug = f"local-{path.name}"
                module_dest = self.vendor_dir / module_slug
                print(f"INFO: Installing local module {path.name}")
                if module_dest.is_dir():
                    print(f"WARN: Module {path.name} already installed")
                else:
                    shutil.copytree(path, module_dest)
            elif module["type"] == "git":
                module_slug = f"{module['version']}-{pathlib.Path(module['url']).stem}"
                module_dest = self.vendor_dir / module_slug
                print(f"INFO: Installing remote module {module_dest.name}")
                if module_dest.is_dir():
                    print(f"WARN: Module {module_dest.name} already installed")
                else:
                    vyos_modular.common.commands.clone_repo(
                        module["url"], module["version"], module_dest
                    )
            else:
                raise RuntimeError(f"Unsupported module type {module['type']}")

            # Process module.yaml file
            with open(module_dest / "module.yaml") as config_fh:
                module_config = yaml.load(config_fh, Loader=yaml.SafeLoader)

            if module_config["version"] != 2:
                raise RuntimeError(f"Unsupported module version!")

            self._modules.append(
                VyosModule(
                    name=module_config["metadata"]["name"],
                    path=module_dest,
                    patches_core=module_config["spec"]["patches_core"],
                    config=module_config,
                )
            )

    @property
    def branch(self) -> str:
        if not self._branch:
            raise RuntimeError("Global config has not been initialised")
        return self._branch

    @property
    def release(self) -> str:
        if not self._release:
            raise RuntimeError("Global config has not been initialised")
        return self._release

    @property
    def modules(self) -> t.List[VyosModule]:
        if not self._modules:
            raise RuntimeError("Global config has not been initialised")
        return self._modules

    @property
    def config(self):
        return None

    @config.setter
    def config(self, value):
        self._raw_config = value
        self._process_config()
