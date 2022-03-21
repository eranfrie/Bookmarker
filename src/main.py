from pathlib import Path
import logging

import version
import config
import opts
import log


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
        print(f"Failed to load config file {config_file} (it is a directory)")
        exit(1)

    # create output (and logs) dir (if doesn't already exist)
    logs_dir = Path(conf["output_dir"], log.LOGS_DIR)
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Failed to create {logs_dir} directory {e}")

    # init logger after create output dir
    log.init_logger(conf["output_dir"])
    logger = logging.getLogger()


if __name__ == "__main__":
    main()
