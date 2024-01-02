# vyos-modular

A tool to create custom vyos installations. This repo recently transitioned to version 2, to access the old version please use the `legacy` branch

## Modules

| Module | Link |
| --------- | ------------------------------------------------------ |
| tailscale | https://github.com/jack-broadway/vyos-module-tailscale |

## Legacy Modules 
| Module | Link |
| --------- | -------------------------------------------------- |
| speedtest | https://github.com/kylechase/vyos-module-speedtest |

## Installation

This tool is only supported on linux as it shells out to linux tools.

Required Tools

```
- git
- rsync
- docker
```

```python3
pip install -r requirements.txt
```

## Usage

Artifacts will output in the bin folder. If unprivileged users dont have access to docker, you will need to run using sudo or root account

### Building an image
```bash
python3 main.py build -c config.yml
```

### Building a base iso
If you dont have access to the LTS isos, vyos-modular can also build you an iso. 
The command below builds an iso from the 1.3.5 tag

```
python3 main.py build_iso -b 1.3.5 -r equuleus
```



