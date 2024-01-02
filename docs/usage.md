# Usage

## Installation

This tool is only supported on linux as it shells out to linux tools.

Required tools on host system

- `git`
- `rsync`
- `docker`

```bash
pip install -r requirements.txt
```

## Commands 

Copy your base iso to the `dist/isos` folder and copy `sample_config.yml` to your desired location.
The sample config below builds with the tailscale module for the 1.3.5 LTS release of equuleus

```yml
# tailscale-1.3.5-config.yml
name: tailscale-1.3.5
vyos_target:
  # This is used to target an appropriate vyos-core version when using modules
  # that patch the core
  branch: 1.3.5
  release: equuleus
  # This is the name of an iso found under dist/isos
  iso: vyos-1.3.5-amd64.iso
modules:
  - type: git
    url: https://github.com/jack-broadway/vyos-module-tailscale.git
    version: main
  # There should be a module.yaml at the location pointed to by path
  - type: local
    path: /path/to/my/in_dev_module
```

Artifacts will output in the bin folder. If unprivileged users dont have access to docker, you will need to run using sudo or root account

```bash
python3 main.py build -c tailscale-1.3.5-config.yml
```

## Building a base ISO

If you dont have access to LTS ISOs or want to target a specific commit, vyos-modular can also be used to build base isos.

```bash
# Build an ISO from the LTS 1.3.5 tag
python3 main.py build_iso -b 1.3.5 -r equuleus
```