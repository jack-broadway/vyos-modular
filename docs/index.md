# vyos-modular

A module based customization suite for vyos

## Direction

Previously, vyos-modular worked by modifying both the `vyos-1x` and `vyos-build` repositories to build a custom iso from complete sources. However, this meant vyos-modular modules were limited by what `vyos-build` could do and you couldn't customize a known good LTS or pre-built ISO.

Version 2 now works by customizing a pre-existing ISO, either an LTS ISO built by the Vyos team, or one you've already built. Under the hood this uses ansible to expand the customization options available to module developers, and is heavily inspired from the [vyos/vyos-vm-images](https://github.com/vyos/vyos-vm-images) project