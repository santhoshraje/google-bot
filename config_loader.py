import json

def get_config_value(config_name, second, first='DEFAULT'):
    with open(config_name, 'r') as f:
        config = json.load(f)
    return config[first][second]

