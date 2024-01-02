import yaml

from vyos_modular.common.config import GlobalConfig
from vyos_modular.core_build.builder import CoreBuilder


def main():
    with open("sample_config.yml") as config_fh:
        modular_config = yaml.load(config_fh, Loader=yaml.SafeLoader)

    config = GlobalConfig()
    config.config = modular_config

    builder = CoreBuilder()
    builder.prepare()
    builder.apply()
    builder.build()


if __name__ == "__main__":
    main()
