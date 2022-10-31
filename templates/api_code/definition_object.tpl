from dataclasses import dataclass

{% for obj in objs %}
@dataclass
class {{ obj.name }}:
    {% for var in obj.variable -%}
    {{ var.name }}: {{ var.type }}
    {% endfor %}
{% endfor %}
