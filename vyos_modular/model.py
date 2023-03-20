import pathlib
import yaml
from typing import List, Optional
from pydantic.dataclasses import dataclass
from pydantic.tools import parse_obj_as
from pydantic import Field


@dataclass
class Repositories:
    apt_entry: str = Field(...)
    gpg_key: str = Field(...)


@dataclass
class PackageURL:
    url: str
    filename: Optional[str] = None


@dataclass
class ModuleConfig:
    name: str
    version: str
    description: Optional[str] = None
    packages: Optional[List[str]] = None
    repositories: Optional[List[Repositories]] = None
    package_urls: Optional[List[PackageURL]] = None


def load_module_config(module_path: pathlib.Path) -> ModuleConfig:
    with open(module_path / "module.yaml") as config_fh:
        module_config_raw = yaml.load(config_fh, Loader=yaml.SafeLoader)
        c = parse_obj_as(ModuleConfig, module_config_raw)
        return c
