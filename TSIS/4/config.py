import os
from configparser import ConfigParser

def load_config(filename=None, section='postgresql'):
    if filename is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, 'database.ini')

    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        return {key: value for key, value in parser.items(section)}

    raise Exception(f'Section {section} not found in the {filename} file')
if __name__ == '__main__':
    config = load_config()
    print(config)