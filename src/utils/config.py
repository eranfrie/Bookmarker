import yaml


CONFIG_FILE = "config.yaml"


def load_config(config_file):
    """Loads a YAML file.

    Raises:
        FileNotFoundError
        IsADirectoryError

    Returns:
        dict
    """
    with open(config_file, "r", encoding="ascii") as f:
        return yaml.safe_load(f)
