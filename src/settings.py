import os
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_PATH = os.path.join(APP_ROOT, 'config.json')
THRIFT_PATH = os.path.join(APP_ROOT, 'src', 'gen-py.tornado')

DOCKER_SOCK = 'unix://var/run/docker.sock'
DOCKER_V = '0.7.6'
TIMEOUT = 10

HTTP_PORT = 8891
THRIFT_PORT = 9891
HOST_IP = '192.168.1.40'

MAX_ATTEMPTS = 3 # can be changed to 10 during holidays