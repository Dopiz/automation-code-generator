import os
import re

from jinja2 import Environment, FileSystemLoader


def camel_to_snake(text: str):
    matches = re.finditer('[A-Z]', text)
    contents = []
    last_start = 0
    for it in matches:
        start, end = it.span()
        if start > 0:
            contents.append(text[last_start:start])
        last_start = start
    contents.append(text[last_start:])
    return '_'.join(contents).lower().replace("-", "_")


class Coder:
    template = "code.tpl"
    output_path = "output/%(class_name)s"

    def __init__(self, data: dict = None):
        self.data = data or {}
        self.output_path = (self.output_path % data).lower()


class CodeGenerator:

    def __init__(self, data: dict):
        self.data = data

    def _process(self) -> Coder:
        raise NotImplementedError

    def generate(self):
        for code in self._process():
            yield code


class Template:

    def __init__(self):
        self.loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates'))
        self.env = Environment(loader=self.loader)

    def _render(self, template_name, **kwargs):
        template = self.env.get_template(template_name)
        return template.render(**kwargs)

    def render_code(self, code):
        return self._render(code.template, **code.data)
