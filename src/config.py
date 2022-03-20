import yaml


CONFIG_FILE = "config.yaml"


def load_config():
    """Loads a YAML file.

    Raises:
        FileNotFoundError

    Returns:
        dict
    """
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)
