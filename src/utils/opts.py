import argparse


PROD_NAME = "Bookmarker"


def get_options():
    parser = argparse.ArgumentParser(description=PROD_NAME)

    parser.add_argument('-v', '--version', action='store_true', default=False,
                        help='Display version')
    parser.add_argument('-c', '--config', metavar='CONFIG', type=str, default=None,
                        help='Path to a YAML config file')

    args = parser.parse_args()
    return args
