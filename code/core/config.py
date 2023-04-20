import yaml


def load_global_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config


global_config = load_global_config("config.yaml")
