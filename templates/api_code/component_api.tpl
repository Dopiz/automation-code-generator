from urllib.parse import urljoin

from api.base_api import BaseAPI
from configurations import {{ component_name }}Config


class {{ ori_component_name }}{{ ori_class_name }}API(BaseAPI):

    base_url = urljoin({{ component_name }}Config.BASE_URL, "{{ class_name.lower() }}/")
    {% for api in apis %}
    {{ api.api_name.upper() }}_PATH = "{{ api.path }}"
    {%- endfor %}
    {% for api in apis %}
    def {{ api.api_name.lower() }}(self, {% for header in api.headers -%}{{ header.name }}: {{ header.type }}, {% endfor -%}
    {%- for body in api.in_path -%}{{ body.name }}: {{ body.type }}, {% endfor -%}
    {%- for body in api.body -%}{{ body.name }}: {{ body.type }}, {% endfor -%}
    {%- for body in api.list_body -%}{{ body.name }}: {{ body.type }}, {% endfor -%}
    {%- for data in api.data -%}{{ data.name }}: {{ data.type }}, {% endfor -%}
    {%- for param in api.params -%}{{ param.name }}: {{ param.type }}, {% endfor -%}
    waiting_time: float = None):
        {%- if api.headers %}
        headers = {
            {%- for header in api.headers %}
            '{{ header.name }}': {{ header.name }},
            {%- endfor %}
        }
        {%- endif %}
        {%- if api.body %}
        body = {
            {%- if api.body -%}
            {%- for body in api.body %}
            '{{ body.name }}': {{ body.name }},
            {%- endfor %}
            {%- endif %}
        }
        {%- elif api.list_body %}
        body = [
            {
                {%- if api.list_body -%}
                {%- for body in api.list_body %}
                '{{ body.name }}': {{ body.name }},
                {%- endfor %}
                {%- endif %}
            }
        ]
        {%- endif %}
        {%- if api.params %}
        params = {
            {%- for param in api.params %}
            '{{ param.name }}': {{ param.name }},
            {%- endfor %}
        }
        {%- endif %}
        {%- if api.data %}
        data = {
            {%- for data in api.data %}
            '{{ data.name }}': {{ data.name }},
            {%- endfor %}
        }
        {%- endif %}
        return self._send_request(
            method='{{ api.method }}',
            url=urljoin(self.base_url, self.{{ api.api_name.upper() }}_PATH{%- if api.in_path -%}.format(
            {%- for path in api.in_path -%}
            {{ path.name }}={{ path.name }},
            {%- endfor -%}
            ){% endif %})
            {%- if api.headers -%},
            headers=headers
            {%- endif %}
            {%- if api.body or api.list_body -%},
            json=body
            {%- endif %}
            {%- if api.params -%},
            params=params
            {%- endif %}
            {%- if api.data -%},
            data=data
            {%- endif %},
            waiting_time=waiting_time
        )
    {% endfor -%}
