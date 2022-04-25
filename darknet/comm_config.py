import configparser
import os
import socket

hostname=socket.gethostname()
# IPAddr=socket.gethostbyname(hostname)
PORT=12345

def read_config(path):
    if os.path.isfile(path):
        config = configparser.ConfigParser()
        config.read(path)
        hostname  = config['SERVER']['Hostname']
        host_port = int(config['SERVER']['Port'])
        host_ip   = config['SERVER']['Host-IP']
        cam_id    = config['CLIENT']['cam_id']
        return hostname, host_port, host_ip, cam_id
    else:
        print("Config File do not exist please Edit :", path)
        create_default_config(path)
        return None


def create_default_config(path):
    config = configparser.ConfigParser()
    # get ipv4 address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    IPAddr = s.getsockname()[0]
    config['SERVER'] = {'Hostname': hostname,
                        'Host-IP': IPAddr,
                        'Port': PORT
                        }
    config['CLIENT'] = {'cam_id': 0}
    with open(path, 'w') as configfile:
        config.write(configfile)


if __name__=="""__main__""":
    hostname, host_port, host_ip, cam_id = read_config("example.ini")
    print(f"{hostname=}, {host_port=}, {host_ip=}, {cam_id=}")