from dataclasses import asdict, dataclass
from typing import List

from .base import Coder, CodeGenerator, camel_to_snake


@dataclass
class Variable:
    name: str
    ori_name: str
    type: str
    require: bool = True


@dataclass
class ApiItem:
    ori_api_name: str
    api_name: str
    path: str
    method: str
    headers: List[Variable] = None
    body: List[Variable] = None
    list_body: list = None
    params: List[Variable] = None
    in_path: List[Variable] = None
    data: List[Variable] = None


@dataclass
class ServiceItem:
    ori_component_name: str
    component_name: str
    ori_class_name: str
    class_name: str
    apis: List[ApiItem] = None

@dataclass
class DefinitionObject:
    name: str
    variable: List[Variable] = None


class ComponentApiCoder(Coder):
    template = "api_code/component_api.tpl"
    output_path = "output/%(ori_class_name)s_api.py"


class ServiceConfigCoder(Coder):
    template = "api_code/config.tpl"
    output_path = "output/%(ori_component_name)s_config.py"


class TestScriptCoder(Coder):
    template = "api_code/test_script.tpl"
    output_path = "output/test_%(ori_class_name)s_api.py"


class DefinitionObjectCoder(Coder):
    template = "api_code/definition_object.tpl"
    output_path = "output/%(name)s_defs.py"


class ApiCodeGenerator(CodeGenerator):

    def _type_mapping(self, ori_type: str):
        return {
            "string": "str",
            "date-time": "str",
            "boolean": "bool",
            "int32": "int",
            "int64": "int",
            "integer": "int",
            "double": "float",
            "number": "float",
            "array": "list"
        }.get(ori_type, ori_type)

    def _process(self) -> Coder:
        definition_objects, data = self._process_data()
        yield ComponentApiCoder(data)
        yield TestScriptCoder(data)
        yield DefinitionObjectCoder(definition_objects)

    def _process_data(self):
        definitions = self.data['definitions']
        definition_objects = []
        for name, item in definitions.items():
            definition_object = DefinitionObject(
                name=name,
                variable=[]
            )
            props = item['properties']
            for prop_name, prop_info in props.items():
                if ref := prop_info.get('$ref'):
                    variable = Variable(
                        ori_name=prop_name,
                        name=camel_to_snake(prop_name),
                        type=ref.split("/")[-1]
                    )
                else:
                    variable = Variable(
                        ori_name=prop_name,
                        name=camel_to_snake(prop_name),
                        type=self._type_mapping(prop_info['type'])
                    )
                definition_object.variable.append(variable)
            definition_objects.append(definition_object)
        definition_objects = {
            'objs': definition_objects,
            'name': self.data['class_name']
        }

        service_item = ServiceItem(
            ori_component_name=self.data['component_name'],
            component_name=camel_to_snake(self.data['component_name']),
            ori_class_name=self.data['class_name'],
            class_name=camel_to_snake(self.data['class_name']),
            apis=[]
        )
        for url, api in self.data['apis'].items():
            try:
                method = list(api.keys())[0]
                api_name = url.split("/")[-1]
                if "{" in api_name:
                    api_name = f"{method}_{url.split('/')[-2]}"
                api_item = ApiItem(
                    ori_api_name=api_name,
                    api_name=camel_to_snake(api_name),
                    path=url,
                    method=method.upper(),
                    headers=[], body=[], in_path=[], params=[], list_body=[], data=[]
                )
                
                parameters = api[method]['parameters']
                for param in parameters:
                    param_in = param['in']
                    if param_in != "body":
                        variable = Variable(
                            ori_name=param['name'],
                            name=camel_to_snake(param['name']),
                            type=self._type_mapping(param['type']),
                            require=param['required']
                        )
                        target = {
                            'path': api_item.in_path,
                            'header': api_item.headers,
                            'query': api_item.params,
                            'formData': api_item.data
                        }.get(param_in)
                        target.append(variable)
                    else:
                        target = api_item.body if method.upper() == "POST" else api_item.params
                        if ref := param['schema'].get('$ref'):
                            ref = ref.split("/")[-1]
                            definition = definitions[ref]
                            require = definition.get('required', [])
                            props = definition['properties']
                            for name, prop in props.items():
                                if ref := prop.get('$ref'):
                                    type_ = ref.split("/")[-1]
                                else:
                                    type_ = self._type_mapping(prop.get('format', prop['type']))
                                variable = Variable(
                                    ori_name=name,
                                    name=camel_to_snake(name),
                                    type=type_,
                                    require=(name in require)
                                )
                                target.append(variable)
                        elif param['schema'].get('type') == "array":
                            ref = param['schema']['items']['$ref'].split("/")[-1]
                            definition = definitions[ref]
                            require = definition.get('required', [])
                            props = definition['properties']
                            for name, prop in props.items():
                                if ref := prop.get('$ref'):
                                    type_ = ref
                                else:
                                    type_ = self._type_mapping(prop.get('format', prop['type']))
                                variable = Variable(
                                    ori_name=name,
                                    name=camel_to_snake(name),
                                    type=type_
                                )
                                api_item.list_body.append(variable)
                        else:
                            variable = Variable(
                                ori_name=param['name'],
                                name=camel_to_snake(param['name']),
                                type=self._type_mapping(param['schema'].get('format', param['schema']['type'])),
                                require=param['required']
                            )
                            target.append(variable)
                service_item.apis.append(api_item)
            except Exception as e:
                print(f"Something Wrong! {url}, {e}")

        return definition_objects, asdict(service_item)