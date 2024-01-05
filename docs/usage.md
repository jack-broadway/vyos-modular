# Usage

## Installation

This tool is only supported on linux as it shells out to linux tools.

Required tools on host system

- `git`
- `rsync`
- `docker`


```bash
# This will place vyos-modular into your python scripts folder

pip install vyos-modular
```

### Dev Install

```bash
pip install -e .
```

## Setting up 

Run the following in an empty directory

```bash
vyos-modular init
```

Copy your base iso to the `resources/isos` folder and modify the generated `config.yml` to suite your needs.


## Building

Artifacts will output in the bin folder. If unprivileged users dont have access to docker, you will need to run using sudo or root account

```bash
vyos-modular build -c tailscale-1.3.5-config.yml
```

## Building a base ISO

If you dont have access to LTS ISOs or want to target a specific commit, vyos-modular can also be used to build base isos.

```bash
# Build an ISO from the LTS 1.3.5 tag
vyos-modular build_iso -b 1.3.5 -r equuleus
```