import argparse
import pathlib

import yaml

import vyos_modular.builder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom Vyos image builder")
    parser.add_argument("--config", "-c", type=pathlib.Path, required=True)
    args = parser.parse_args()

    with open(args.config) as config_fh:
        config = yaml.load(config_fh, Loader=yaml.SafeLoader)

    match config["vyos_branch"]:
        case "equuleus":
            builder = vyos_modular.builder.EquuleusBuilder(config)
        case "current":
            builder = vyos_modular.builder.SaggitaBuilder(config)
        case other:
            raise ValueError(f"Unsupported build branch {config['vyos_branch']}")

    builder.run()
