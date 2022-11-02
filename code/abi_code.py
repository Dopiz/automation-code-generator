from dataclasses import asdict, dataclass
from typing import List

from .base import CodeGenerator, Coder, camel_to_snake


@dataclass
class Variable:
    value: str
    key: str
    type_: str


@dataclass
class AbiItem:
    name: str
    type_: str
    variables: List[Variable] = None


@dataclass
class ServiceItem:
    component_name: str
    class_name: str
    chain_name: str
    abis: List[AbiItem]


class AbiCoder(Coder):
    template = "abi_code/component_abi.tpl"
    output_path = "output/%(class_name)s_abi.py"


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
            component_name=self.data['component_name'],
            class_name=self.data['class_name'],
            chain_name=self.data['chain_name'],
            abis=[]
        )
        for item in self.data['abis']:
            if item['type'] != "function":
                continue
            abi_item = AbiItem(
                type_=item.get('stateMutability', None),
                name=item['name'],
                variables=[]
            )
            for input_ in item['inputs']:
                if input_['name']:
                    variable = Variable(
                        value=camel_to_snake(input_['name']),
                        key=input_['name'],
                        type_=self._type_mapping(input_['type']),
                    )
                    abi_item.variables.append(variable)
            service_item.abis.append(abi_item)
        return asdict(service_item)
