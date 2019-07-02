#!/user/bin/env python
import subprocess
import logging

SPEEDTEST_CMD = 'speedtest-cli'
LOG_FILE = 'speedtest.log'

def main():
  setupLogging()
  try:
    ping, download, upload = getSpeedtestResults()
  except ValueError as err:
    logging.info(err)
  else:
    logging.info("%5.1f %5.1f %5.1f", ping, download, upload)

def setupLogging():
  logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M",
    )

def getSpeedtestResults():

    # Run test and parse results.
    # Returns tuple of ping speed, download speed, and upload speed,
    # or raises ValueError if unable to parse data.

    ping = download = upload = None
    speedtestOutput = subprocess.Popen([SPEEDTEST_CMD, "--simple"], stdout = subprocess.PIPE, shell = True, universal_newlines=True)
    
    for line in speedtestOutput.stdout:
        label, value, unit = line.split()
        if 'Ping' in label:
            ping = float(value)
        elif 'Download' in label:
            download = float(value)
        elif 'Upload' in label:
            upload = float(value)

    if all((ping, download, upload)): # if all 3 values were parsed
        return ping, download, upload
    else:
        raise ValueError('TEST FAILED')

if __name__ == '__main__':
  main()
