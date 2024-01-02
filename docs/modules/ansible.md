## Ansible Roles

vyos-modular supports modification of the system through ansible. Modules have access to the squashfs filesystem that gets mounted during vyos boot to become the root filesystem.

### Ansible Variables
The following ansible variables are available to your roles

| variable name | description | sample value |
| -------------- | ------------------------- | ------------ |
| `vyos_cd_root` | The mount path of the ISO | `/mnt/cdrom` |
| `vyos_install_root` | The root path to the unpacked root filesystem | `/mnt/inst_root` |
| `vyos_version` | The full version string of the vyos image | `1.4-rolling-202307250317` |
| `vyos_debian_codename` | The debian release name for this vyos version | `bookworm` |
| `vyos_release` | The vyos release name for this version | `sagitta` |


### Example Role

The following role is taken from [kylechase/vyos-module-speedtest](https://github.com/kylechase/vyos-module-speedtest) as it is a good example of a common module goal to install new packages

#### tasks/main.yml
```yml
- name: Copy speedtest GPG repo key
  ansible.builtin.copy:
    src: files/ookla_speedtest-cli-archive-keyring.gpg
    dest: "{{ vyos_install_root }}/usr/share/keyrings/ookla_speedtest-cli-archive-keyring"
    mode: '0644'

- name: Dearmour speedtest GPG key
  ansible.builtin.command: chroot {{ vyos_install_root }} gpg --dearmor /usr/share/keyrings/ookla_speedtest-cli-archive-keyring

- name: Copy speedtest repo config
  ansible.builtin.template:
    src: templates/ookla-speedtest.list.j2
    dest: "{{ vyos_install_root }}/etc/apt/sources.list.d/ookla-speedtest.list"
    mode: '0644'

- name: apt-get update
  command: chroot {{ vyos_install_root }} apt-get update

- name: install speedtest
  command: chroot {{ vyos_install_root }} apt-get install -y speedtest
  
- name: apt-get clean
  command: chroot {{ vyos_install_root }} apt-get clean

- name: delete apt lists from cache
  command: chroot {{ vyos_install_root }} rm -rf /var/lib/apt/lists/

- name: Delete ookla-speedtest.list
  file:
    path: "{{ vyos_install_root }}/etc/apt/sources.list.d/ookla-speedtest.list"
    state: absent

- name: Delete ookla_speedtest-cli-archive-keyring.gpg
  file:
    path: "{{ vyos_install_root }}/usr/share/keyrings/ookla_speedtest-cli-archive-keyring.gpg"
    state: absent
```

#### templates/ookla-speedtest.list.j2
```console
deb [signed-by=/usr/share/keyrings/ookla_speedtest-cli-archive-keyring.gpg] https://packagecloud.io/ookla/speedtest-cli/debian/ {{ vyos_debian_codename }} main
```