# vyos-modular

A tool to create custom vyos installations

## Modules

| Module | Link |
| --------- | ------------------------------------------------------ |
| tailscale | https://github.com/jack-broadway/vyos-module-tailscale |
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

```bash
# Because the container modifies the build folder as root
# the script cant delete this folder on repeated runs
rm -rf build/ 
python3 main.py -c config.yml
```

Artifacts will output in the bin folder

## Roadmap

- Add support for configuring the tailscale listening port from the vyos cli
- Properly handle the case where we are bringing up tailscale for the first time, instead of just catching TimeoutExpired
- Handle vyos patches in modules across versions