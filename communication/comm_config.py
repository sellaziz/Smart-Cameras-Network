import configparser
import os

def read_config(path):
    if os.path.isfile(path):
        config = configparser.ConfigParser()
        config.read(path)
        hostname           = config['SERVER']['Hostname']
        port               = int(config['SERVER']['Port'])
        buffersize         = int(config['SERVER']['buffersize'])
        client_name        = config['CLIENT']['Name']
        client_orientation = config['CLIENT']['orientation']
        return hostname, port, buffersize, client_name, client_orientation
    else:
        print("Config File do not exist please Edit :", path)
        create_default_config(path)
        return None


def create_default_config(path):
    config = configparser.ConfigParser()
    config['SERVER'] = {'Hostname': 'localhost',
                        'Port': '65432',
                        'buffersize': '1024'
                        }
    config['CLIENT'] = {'Name': 'localhost',
                        'orientation': 'none'}
    with open(path, 'w') as configfile:
        config.write(configfile)


if __name__=="""__main__""":
    hostname, port, buffersize, client_name, client_orientation = read_config("example.ini")
    print(f"{hostname=}, {port=}, {buffersize=}, {client_name=}, {client_orientation=}")