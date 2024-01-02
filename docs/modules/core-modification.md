# Core Modification

For more complicated modules (i.e where you want to add functionality to the vyos cli) you will need to patch the core vyos package.
vyos-modular has two mechanisms for this, the overlay system and the git patch system. Both systems operate on the [vyos/vyos-1x](https://github.com/vyos/vyos-1x) repository.
To enable for your module, set `patches_core: true` in your module spec section.

For a sample module, see [jack-broadway/vyos-module-tailscale](https://github.com/jack-broadway/vyos-module-tailscale) as it uses both the overlay and core patching components

## Overlay

Create `vyos-core/{vyos_release}/overlay` folder in your module. Any directories created under here will be placed into the `vyos-1x` repository before building.
More information on creating commands can be found in the vyos documentation [Development - VyOS 1.4.x (sagitta)](https://docs.vyos.io/en/sagitta/contributing/development.html).


For example, to create a new command tree and its python handler for a custom service, create a directory structure as follows:

```console
├── vyos-core
    ├── sagitta
        ├── overlay
            │── src
            │   ├── conf_mode
            │       ├── service_myservice.py
            │── interface-definitions
                ├── service_myservice.xml.in
```

If your overlay doesnt need to change between vyos releases, simply symlink the other releases to your overlay

```bash
ln -s vyos-core/sagitta/overlay vyos-core/current/overlay
```

## Patching

If your module needs to modifying existing functionality of vyos, git patches can be used. 

To create, clone your target version of the `vyos-1x` repository and make your changes. Then use `git diff > my_patch.patch` and put in the appropriate release patch folder in your module

```console
├── vyos-core
    ├── sagitta
    │   ├── patches
    │       │── my_sagitta_patch.patch
    ├── current
        ├── patches
            ├── my_current_patch.patch
```