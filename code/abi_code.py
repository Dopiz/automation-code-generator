from dataclasses import asdict, dataclass
from typing import List

from .base import Coder, CodeGenerator, camel_to_snake


@dataclass
class Variable:
    name: str
    ori_name: str
    type: str
    ori_type: str


@dataclass
class AbiItem:
    type: str
    name: str
    ori_name: str
    inputs: List[Variable] = None


@dataclass
class ServiceItem:
    ori_component_name: str
    component_name: str
    ori_class_name: str
    class_name: str
    chain_name: str
    abis: List[AbiItem]


class AbiCoder(Coder):
    template = "abi_code/component_abi.tpl"
    output_path = "output/%(ori_class_name)s_abi.py"


class AbiCodeGenerator(CodeGenerator):

    def _type_mapping(self, ori_type: str):
        return {
            "address": "str",
            "uint8": "int",
            "uint16": "int",
            "uint256": "int",
            "bool": "bool",
            "bytes4": "str",
            "bytes32": "str",
            "address[]": list
        }.get(ori_type, ori_type)

    def _process(self) -> Coder:
        data = self._process_data()
        yield AbiCoder(data)

    def _process_data(self):
        service_item = ServiceItem(
            ori_component_name=self.data['component_name'],
            component_name=camel_to_snake(self.data['component_name']),
            ori_class_name=self.data['class_name'],
            class_name=camel_to_snake(self.data['class_name']),
            chain_name=self.data['chain_name'],
            abis=[]
        )
        for item in self.data['abis']:
            if item['type'] not in ["function"]:
                continue
            abi_name = camel_to_snake(item['name']) if "_" not in item['name'] else item['name']
            abi_item = AbiItem(
                type=item.get('stateMutability', None),
                name=abi_name,
                ori_name=item['name'],
                inputs=[]
            )
            for input_ in item['inputs']:
                if input_['name']:
                    var = Variable(
                        name=camel_to_snake(input_['name']),
                        ori_name=input_['name'],
                        type=self._type_mapping(input_['type']),
                        ori_type=input_['type']
                    )
                    abi_item.inputs.append(var)
            service_item.abis.append(abi_item)
        return asdict(service_item)
