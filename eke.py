#!/usr/bin/env python

# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import logging
import time
import json

#third party libs
from daemon import runner
from lsanomaly import lsanomaly as LS

from Pubnub import Pubnub
import sys

import pandas as pd
import numpy as np
import sklearn

class App():
    
    def readKeys(self):
        myvars = {}
        with open("keys") as myfile:
            for line in myfile:
                name, var = line.partition("=")[::2]
                myvars[name.strip()] = "".join(var.split())


        self.publish_key = myvars["publish_key"]
        self.subscribe_key = myvars["subscribe_key"]
        self.secret_key = myvars["secret_key"]


    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/eke.pid'
        self.channel_sub = 'hello_world'
        self.pidfile_timeout = 5

        self.df = pd.DataFrame(columns = ['temp'])

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
        logger.info(message)
        pass

    # Asynchronous usage
    def callback(self, message, channel):
        # load stuff into LS or DBScan
        anomalymodel = LS.LSAnomaly(rho=1, sigma=.5)

        s = message
        logger.info(float(s['temp']))
        self.df.loc[self.df.values.size] = float(s['temp'])
        
        if self.df.values.size > 10:
            ### This is no good! I need to train the data
            if np.std(self.df.values) > 1:
                pass
                
            #print np.array(self.df.values)
            df_scale = self.df['temp'].values#.reshape(self.df.values.size,1)#sklearn.preprocessing.scale(self.df['temp'].values)

            df_scale = df_scale.reshape(df_scale.shape[0],1)

            anomalymodel.fit(df_scale)
            anomalymodel.predict(df_scale)#,columns=['outcome']
            df2 = pd.DataFrame(anomalymodel.predict(df_scale),columns=['outcome'])
            self.df['outcome'] = df2
            print self.df2
            for i in self.df[self.df['outcome'] == 'anomaly'].values:
                logger.error("Anomaly Detected! -- " + i[0])
                
                
            del self.df
            del anomalymodel
            del df_scale
            del df2
            self.df = pd.DataFrame(columns = ['temp'])
                
                

    def error(self, message):
        print("ERROR : " + str(message))


    def connect(self, message):
        print("CONNECTED")


    def reconnect(self, message):
        print("RECONNECTED")


    def disconnect(self, message):
        print("DISCONNECTED")

    def run(self):

        logger.info("Eke server started!")

        
        self.pubnub.subscribe(self.channel_sub, 
                              callback=self.callback, 
                              error=self.callback,
                              connect=self.connect, 
                              reconnect=self.reconnect, 
                              disconnect=self.disconnect
                              )


app = App()
logger = logging.getLogger("EkeLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/tmp/eke.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
