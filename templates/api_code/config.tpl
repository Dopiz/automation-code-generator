# defaults.py
class {{ ori_component_name }}Config:
    BASE_URL = "https://{{ domain_url }}"

# test.py
class {{ ori_component_name }}Config(defaults.{{ ori_component_name }}Config):
    BASE_URL = "https://{{ domain_url }}"