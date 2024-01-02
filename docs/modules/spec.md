# Module Specification

In the root of a module there needs to be a `module.yaml` that has information needed by `vyos-modular`

## Best Practices

- Tag your modules so that users can target specific versions in their config.
- Try to make your ansible roles work regardless of version by using the available variables to determine target vyos version
- Try to make your core patches as generic as possible so they have less chance of breaking between updates

## Example Structure

### module.yaml
```yml
# This is always version 2
version: 2
metadata:
  name: my-first-module
spec:
  # Patches core is set to true if you want to perform modifications on the vyos-1x code
  patches_core: true
  # These roles are run in the order they appear in your spec
  ansible_roles:
    - role_a
    - role_b
```

### Directory Structure

```console
├── roles
│   ├── role_a
│   │   ├── tasks
│   │       │── main.yml
│   ├── role_b
│   │   ├── tasks
│   │   │   │── main.yml
│   │   ├── templates
│   │       ├── config.yml.j2
├── vyos-core
│   ├── equuleus
│   │   ├── overlay
│   │   │   ├── interface_definitions
│   │   │       ├── service_newservice.xml.in
│   │   ├── patches
│   │       ├── my_equuleus_feature.patch
│   ├── sagitta
│   │   ├── overlay -> ../equuleus/overlay
│   │   ├── patches
│   │       ├── my_sagitta_feature.patch
│   ├── current -> sagitta
└── module.yaml
```

