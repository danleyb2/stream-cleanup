import logging
import os
import shutil
import time
import sys
from configobj import ConfigObj


LOG_LEVEL = os.environ.get('LOGGING', 'INFO').upper()

logging.basicConfig(
    stream=sys.stdout,
    level=LOG_LEVEL,
    style='{',
    format="{asctime} {levelname} {name} {threadName} : {message}")

lgr = logging.getLogger(__name__)


CONFIG_FILE = '/user-data/config.ini'

def cleanup(cameras):
    """
    Delete camera screenshots dirs
    """

    for camera in cameras:
        lgr.info(f'Cleaning up Camera: {camera}')
        screenshots_dir = f'/user-data/{camera}'
        os.remove(screenshots_dir)

        try:
            shutil.rmtree(screenshots_dir)
        except OSError as e:
            lgr.error(f"Error Deleting: {e.filename} - {e.strerror}. Skipped.")



def disk_check(limit):
    """
    Check disk usage as a percentage
    """

    total, used, free = shutil.disk_usage(__file__)
    lgr.debug(f'Total: {total}, Used: {used}, Free: {free} ')
    usage = used/total*100

    lgr.debug(f'Usage :{usage}%')

    return usage > limit



if __name__ == '__main__':
    interval = int(os.getenv('INTERVAL', 30))
    percentage = int(os.getenv('PERCENTAGE', 90))

    if not os.path.exists(CONFIG_FILE):
        lgr.error('config.ini not found, did you forget to mount the stream volume?')
        exit(1)

    config = ConfigObj('config.ini')
    cameras = config['cameras'].sections
    while True:
        disk_full = disk_check(percentage)
        if disk_full:
            cleanup(cameras)
        time.sleep(interval)
