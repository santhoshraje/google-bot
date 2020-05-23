import json

def get_config_value(second, first='DEFAULT', config_name = 'config.json'):
    with open(config_name, 'r') as f:
        config = json.load(f)
    return config[first][second]

