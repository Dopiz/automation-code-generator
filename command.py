import codecs
import json
from os import makedirs
from os.path import dirname, exists

import click
import requests

from code import AbiCodeGenerator, ApiCodeGenerator, Template


def write(dist, content):
    dir_ = dirname(dist)
    if not exists(dir_):
        makedirs(dir_)
    with codecs.open(dist, 'w', 'utf-8') as f:
        f.write(content)


@click.command()
@click.option('-f', '--doc-file', required=True, help='Document json file or http url.')
@click.option('-t', '--templates', required=True, help='CodeGen Template.')
@click.option('-cp', '--component-name', required=True, help='Component Name.')
@click.option('-cl', '--class-name', required=True, help='Class Name.')
@click.option('-ch', '--chain-name', default='BSC', help='Chain Name.')
def generate(doc_file, templates, component_name, class_name, chain_name):

    if "http" in doc_file:
        spec = requests.get(doc_file).json()
    else:
        spec = json.load(open(doc_file))

    data = {
        'component_name': component_name,
        'class_name': class_name
    }
    if templates == "api":
        data.update({
            'apis': spec['paths'],
            'definitions': spec['definitions']
        })
        generator = ApiCodeGenerator(data)
    elif templates == "abi":
        data.update({
            'chain_name': chain_name,
            'abis': spec
        })
        generator = AbiCodeGenerator(data)
    else:
        print("Template not exist.")
        return
    
    template = Template()
    for code in generator.generate():
        source = template.render_code(code)
        write(code.output_path, source)


generate()
