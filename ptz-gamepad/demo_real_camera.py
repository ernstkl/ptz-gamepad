import yaml
from ptzipcam.ptz_camera import PtzCam

config_file = 'cam_config.yml'

with open(config_file, 'r') as f:
    cam_config = yaml.safe_load(f)

# ptz camera networking constants
IP = cam_config['IP']
PORT = cam_config['PORT']
USER = cam_config['USER']
PASS = cam_config['PASS']

ptz = PtzCam(IP, PORT, USER, PASS)

# do some movement

ptz.twitch()

