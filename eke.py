#!/usr/bin/env python

# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import logging
import time



#third party libs
from daemon import runner
from lsanomaly import lsanomaly as LS

from Pubnub import Pubnub
import sys

class App():
    
    def readKeys(self):
        myvars = {}
        with open("keys") as myfile:
            for line in myfile:
                name, var = line.partition("=")[::2]
                myvars[name.strip()] = var.rstrip()

        self.publish_key = myvars["publish_key"].rstrip()
        self.subscribe_key = myvars["subscribe_key"].rstrip()
        self.secret_key = myvars["secret_key"].rstrip()


    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/testdaemon.pid'
        self.channel_sub = 'hello_world'
        self.pidfile_timeout = 5

        self.publish_key = ''
        self.subscribe_key = ''
        self.secret_key = ''
        self.cipher_key = ''
        self.ssl_on = False

        self.readKeys()

        self.pubnub = Pubnub(publish_key=self.publish_key, 
                             subscribe_key=self.subscribe_key,
                             secret_key=self.secret_key, 
                             cipher_key=self.cipher_key, 
                             ssl_on=self.ssl_on)

    def anomaly(self, message):
        logger.error(message)
        pass

    # Asynchronous usage
    def callback(self, message, channel):
        # load stuff into LS or DBScan
        anomalymodel = LS.LSAnomaly(rho=1, sigma=.5)
        logger.error(message)


    def error(self, message):
        print("ERROR : " + str(message))


    def connect(self, message):
        print("CONNECTED")


    def reconnect(self, message):
        print("RECONNECTED")


    def disconnect(self, message):
        print("DISCONNECTED")

    def run(self):
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warn("Warning message")
        logger.error("Error message")

        self.pubnub.subscribe(self.channel_sub, 
                              callback=self.callback, 
                              error=self.callback,
                              connect=self.connect, 
                              reconnect=self.reconnect, 
                              disconnect=self.disconnect
                              )

'''
        while True:
            #Main code goes here ...
            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs

            logger.info("Info message")
            logger.warn("Warning message")
            logger.error("Error message")

            time.sleep(10)
'''

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/tmp/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
