import version
import config


def main():
    v = version.get_version()
    print(f"EasyBookmarks Version {v}")

    try:
        conf = config.load_config()
    except FileNotFoundError:
        print(f"Config file {config.CONFIG_FILE} not found")


if __name__ == "__main__":
    main()
