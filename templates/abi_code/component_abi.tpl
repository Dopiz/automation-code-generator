from abi.base_abi import BaseABI
from configurations import GeneralConfig, {{ component_name }}Config


class {{ class_name }}ABI(BaseABI):

    def __init__(self):
        super().__init__(
            chain_id=GeneralConfig.{{ chain_name }}_CHAIN_ID,
            node_url=GeneralConfig.{{ chain_name }}_NODE_URL,
            config={{ component_name }}Config.{{ class_name.upper() }}_CONTRACT
        )
    {% for abi in abis %}
    def {{ abi.name }}(self{%- if abi.type_ != "view" -%}, address: str, private_key: str{%- endif -%}{% for input in abi.variables -%}, {{ input.value }}: {{ input.type_ }}{% endfor -%}):
        {%- if abi.type_ != "view" %}
        return self._send_write_request(
            address=address,
            private_key=private_key,
        {%- else %}
        return self._send_read_request(
        {%- endif %}
        {%- if abi.variables %}
            abi=self._contract.functions.{{ abi.name }}(
                {%- for input in abi.variables %}
                {{ input.key }}={{ input.value }},
                {%- endfor %}
            )
        )
        {%- else %}
            abi=self._contract.functions.{{ abi.name }}()
        )
        {%- endif %}
    {% endfor -%}
