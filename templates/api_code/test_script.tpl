import allure
import pytest

from api.{{ component_name }} import {{ component_name }}{{ class_name }}API
from tests.dataprocess import DataProcess

data_process = DataProcess("{{ component_name }}/{{ class_name }}")


class TestCase:

    {{ class_name }}_api = {{ component_name }}{{ class_name }}API()
    {% for api in apis %}
    @pytest.mark.parametrize('data', data_process.read_data("{{ api.api_name.lower() }}"))
    def test_{{ api.api_name.lower() }}(self, data):
        {% if api.headers or api.body or api.params %}
        res = self.{{ class_name }}_api.{{ api.api_name.lower() }}(
            {%- for header in api.headers %}{{ header.name }}=data['{{ header.name }}'],{%- endfor %}
            {%- for body in api.body %}
            {{ body.name }}=data['{{ body.name }}'],
            {%- endfor %}
            {%- for param in api.params %}
            {{ param.name }}=data['{{ param.name }}'],
            {%- endfor %}
        ).json()
        {% else %}
        res = self.{{ class_name }}_api.{{ api.api_name.lower() }}().json()
        {% endif %}
        assert res['result'] == data['result']
        ...
    {% endfor %}