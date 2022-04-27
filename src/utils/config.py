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
    # pylint: disable=W1514 (unspecified-encoding)
    with open(config_file, "r") as f:
        return yaml.safe_load(f)
