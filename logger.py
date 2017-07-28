import logging
import sys

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
file_handler = logging.FileHandler(filename='nh_deploy.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level = logging.DEBUG,
    format = LOG_FORMAT,
    filemode = 'a'.capitalize,
    handlers = [file_handler, stdout_handler]
)

def getLogger():
    return logging.getLogger()