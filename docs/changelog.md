# Changelog


## v2.1.0

- Fixes [Issue #7](https://github.com/jack-broadway/vyos-modular/issues/7) where circinus (current) version isnt detected properly
- Fixes [Issue #9](https://github.com/jack-broadway/vyos-modular/issues/9) where inplace upgrades wouldnt work
- Packages as a proper python package now
- Ties customize docker image to package version
- Adds an `init` command to vyos-modular so you can run the tool without requiring the directory structure from git

## v2.0.0

- Initial rewrite
- Uses ansible to perform iso customization
- Operates on existing ISOs instead of building entirely new ISOs from source