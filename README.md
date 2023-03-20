# vyos-modular

A tool to create custom vyos installations

## Modules

| Module | Link |
| --------- | ------------------------------------------------------ |
| tailscale | https://github.com/jack-broadway/vyos-module-tailscale |
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

```bash
# Because the container modifies the build folder as root
# the script cant delete this folder on repeated runs
rm -rf build/ 
python3 main.py -c config.yml
```

Artifacts will output in the bin folder

## Module Config

The exact module config yaml format is described by [`vyos_modular/model.py`](./vyos_modular/model.py).

### `name`

**Required** `str`

The name of the module

``` yaml
name: tailscale
```

### `version`

**Required** `str`

The version of the module

``` yaml
version: 1.0.0
```

### `description`

*Optional* `str`

A short summary of what the module is for.

``` yaml
description: Installs and configures tailscale on VyOS
```

### `packages`

*Optional* `list of strings`

A list of packages names to install.

``` yaml
packages:
  - git
  - vim
```

### `package_urls`

*Optional* List of `url` and (optionally) `filename`

Install packages directly from a url.

``` yaml
package_urls:
  - url: https://github.com/mozilla/sops/releases/download/v3.7.3/sops_3.7.3_amd64.deb

# or, if the filename cannot be determined from the URL automatically

package_urls:
  - url: https://github.com/mozilla/sops/releases/download/v3.7.3/sops_3.7.3_amd64.deb
    filename: sops.deb
```

### `repositories`

*Optional* List of `apt_entry` and `gpg_key`

A list of repositories to add to apt.

``` yaml
repositories:
  - apt_entry: "deb https://pkgs.tailscale.com/stable/debian bullseye main"
    gpg_key: "tailscale.gpg"
```

### `vyos_build_script`

*Optional* `str`

An arbitrary script to execute before the build starts. The current working directory of the script is the vyos-build dir.

``` yaml
vyos_build_script: |
  set -e
  MFT_VERSION=4.23.0-104
  wget -q https://www.mellanox.com/downloads/MFT/mft-${MFT_VERSION}-x86_64-deb.tgz -O mft-deb.tgz
  tar -zxvf mft-deb.tgz
  mv mft-${MFT_VERSION}-x86_64-deb/DEBS/*.deb packages/
  rm -rf mft-${MFT_VERSION}-x86_64-deb mft-deb.tgz
  rm -rf packages/mft-pcap_${MFT_VERSION}_amd64.deb
```

### `vyos_core_script`

*Optional* `str`

An arbitrary script to execute before the build starts. The current working directory of the script is the vyos-core dir.

See `vyos_build_script` for example


## Roadmap

- Add support for configuring the tailscale listening port from the vyos cli
- Properly handle the case where we are bringing up tailscale for the first time, instead of just catching TimeoutExpired
- Handle vyos patches in modules across versions
