import importlib.resources
import shutil

import jinja2

import vyos_modular.common.commands
from vyos_modular.common.config import GlobalConfig


class CustomBuilder:
    def __init__(self):
        self.ansible_roles = []
        self.config = GlobalConfig()

    def prepare(self):
        # Remove any existing roles
        shutil.rmtree(self.config.dist_dir / "roles")

        for module in self.config.modules:
            if "ansible_roles" in module.config["spec"]:
                # We need to copy each role into the dist folder so that its mounted in the container
                roles = module.config["spec"]["ansible_roles"]
                for role in roles:
                    role_slug = f"{module.name}-{role}"
                    role_src = module.path / "roles" / role
                    role_dst = self.config.dist_dir / "roles" / role_slug
                    shutil.copytree(role_src, role_dst)
                    self.ansible_roles.append(role_slug)

        # Build the ansible playbook from template, including the additional roles from our module
        with importlib.resources.path(
            "vyos_modular.templates", "playbook.yml.j2"
        ) as template_path:
            with open(template_path, "r") as template_fh:
                template = template = jinja2.Template(template_fh.read())

        with open(self.config.dist_dir / "playbook.yml", "w") as output_fh:
            output_fh.write(
                template.render(
                    roles=self.ansible_roles,
                    iso_name=self.config._raw_config["vyos_target"]["iso"],
                )
            )

    def build(self):
        self.prepare()

        vyos_modular.common.commands.run_vyos_customize_cmd(
            ["ansible-playbook", "playbook.yml"], self.config.dist_dir
        )
