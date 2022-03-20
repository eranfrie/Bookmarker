import version
import config
import opts


def main():
    options = opts.get_options()
    if options.version:
        v = version.get_version()
        print(f"EasyBookmarks Version {v}")
        exit(0)

    config_file = config.CONFIG_FILE if not options.config else options.config
    try:
        conf = config.load_config(config_file)
    except FileNotFoundError:
        print(f"Config file {config_file} not found")
        exit(1)
    except IsADirectoryError:
        print(f"Failed to load config file {config_file} - it is a directory")
        exit(1)


if __name__ == "__main__":
    main()
