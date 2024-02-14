# Changelog
## v2.3.0
- Allow the chroot environment to be able to install dependencies for packages

## v2.2.0
- Allows symlinks to be followed in modules

## v2.1.2
- Fixes [Issue #11](https://github.com/jack-broadway/vyos-modular/issues/11) where the sagitta version check didnt work on branch head builds

## v2.1.1
- Fixes [Issue #10](https://github.com/jack-broadway/vyos-modular/issues/10) where the publish package didnt work
- Fixes bug where if you changed config to only include modules that didnt patch vyos core, you'd still get the previously vyos-1x package installed 

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