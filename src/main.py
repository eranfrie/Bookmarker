from pathlib import Path
import logging
import sys

from utils import config, log, opts, version
from app.app import App
from app.app_api import AppAPI
from data.sqlite import Sqlite
from server.bookmarks import Server


def main(override_config):
    options = opts.get_options()
    if options.version:
        v = version.get_version()
        print(f"{opts.PROD_NAME} Version {v}")
        sys.exit(0)

    config_file = config.CONFIG_FILE if not options.config else options.config
    try:
        conf = config.load_config(config_file)
    except FileNotFoundError:
        print(f"Config file {config_file} not found")
        sys.exit(1)
    except IsADirectoryError:
        print(f"Failed to load config file {config_file} (it is a directory)")
        sys.exit(1)
    # override config
    for k, v in override_config.items():
        conf[k] = v

    # create output (and logs) dir (if doesn't already exist)
    output_dir = conf["output_dir"]
    logs_dir = Path(output_dir, log.LOGS_DIR)
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
    # pylint: disable=W0703
    except Exception as e:
        print(f"Failed to create {logs_dir} directory {e}")

    # init logger after create output dir
    log.init_logger(output_dir, conf["console_log_level"])
    logger = logging.getLogger()

    logger.info("start running")
    db_filename = Path(output_dir, "bookmarks.db")
    db = Sqlite(db_filename)
    server = Server(db)
    app = App(server)
    AppAPI(app).run(conf["host"], conf["port"])  # blocking


if __name__ == "__main__":
    main({})
