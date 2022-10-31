from abi.base_abi import BaseABI
from configurations import GeneralConfig, {{ ori_component_name }}Config


class {{ ori_class_name }}ABI(BaseABI):

    def __init__(self):
        super().__init__(
            chain_id=GeneralConfig.{{ chain_name }}_CHAIN_ID,
            node_url=GeneralConfig.{{ chain_name }}_NODE_URL,
            config={{ ori_component_name }}Config.{{ ori_class_name.upper() }}_CONTRACT
        )
    {% for abi in abis %}
    def {{ abi.ori_name }}(self{%- if abi.type != "view" -%}, address: str, private_key: str{%- endif -%}{% for input in abi.inputs -%}, {{ input.name }}: {{ input.type }}{% endfor -%}):
        {%- if abi.inputs -%}
        {% if abi.type == "view" %}
        return self._send_read_request({% else %}
        return self._send_write_request(
            address=address,
            private_key=private_key,
        {%- endif %}
            abi=self._contract.functions.{{ abi.ori_name }}(
                {%- for input in abi.inputs %}
                {{ input.ori_name }}={{ input.name }},
                {%- endfor %}
            )
        )
        {% else %}
        return self._send_request(
            abi=self._contract.functions.{{ abi.ori_name }}()
        )
        {% endif %}
    {%- endfor -%}
