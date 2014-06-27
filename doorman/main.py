import argparse, os, logging, appdirs
from doorman import Doorman, DoormanException

DEFAULT_CONFIG_PATH = appdirs.user_config_dir("doorman")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_PATH, "doorman.yml")
DEFAULT_CONFIG = ""

def is_default_config(config_file):
    """
    Return whether or not config_file is the default config file.

    config_file is the default config file when:
    - config_file is at the location of DEFAULT_CONFIG_FILE
    - The contents of config_file are the same as the value of DEFAULT_CONFIG

    :param config_file: string
    """
    if not config_file == DEFAULT_CONFIG_FILE:
        return False

    if not os.path.exists(DEFAULT_CONFIG_PATH):
        os.makedirs(DEFAULT_CONFIG_PATH)

    if not os.path.exists(DEFAULT_CONFIG_FILE):
        with open(DEFAULT_CONFIG_FILE, "w") as f:
            f.write(DEFAULT_CONFIG)
        os.chmod(DEFAULT_CONFIG_FILE, 0o600) 
        # 0o600 is -rw------- which means rw for only the owner, this is the safest

        return True

    return open(DEFAULT_CONFIG_FILE, "r").read() == DEFAULT_CONFIG

def create_parser():
    """
    Create an argument parser for doorman. 

    This is the structure:
    usage: doorman [-h] [-u | -s] [-v] [-c CONFIG_FILE]

    Doorman keeps your secret things

    optional arguments:
      -h, --help            show this help message and exit
      -u, --unsecret        Open all secret things
      -s, --secret          Hide all secret things
      -v, --verbose         Show all messages
      -c CONFIG_FILE, --config CONFIG_FILE
                            Config file
    """
    parser = argparse.ArgumentParser(description='Doorman keeps your secret things')
    parser.set_defaults(status=True)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-u', '--unsecret', action="store_false", dest="status", help='Open all secret things')
    group.add_argument('-s', '--secret', action="store_true", dest="status", help='Hide all secret things')
    parser.add_argument('-v', '--verbose', action="store_true", dest="verbose", help='Show all messages')
    parser.add_argument('-c', '--config', action="store", dest="config_file",
                        default=DEFAULT_CONFIG_FILE, help='Config file')
    return parser

def main():
    """
    Main function
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.WARN)

    if not is_default_config(args.config_file):
        try:
            doorman = Doorman(args.status, os.path.abspath(args.config_file))
            doorman.run()
        except DoormanException, e:
            logging.error(e)
            parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
