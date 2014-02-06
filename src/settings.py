import os.path
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_PATH = os.path.join(APP_ROOT, 'config.json')

DOCKER_SOCK = 'unix://var/run/docker.sock'
DOCKER_V = '0.7.6'
TIMEOUT = 10

HTTP_PORT = 8891
HOST_IP = '192.168.1.40'