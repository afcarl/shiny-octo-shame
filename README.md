###PubNub & Tessel Hackathon Entry###

*eke.py* is a simple server daemon written in python that listens to a Pubnub channel being broadcast from a Tessel sensor device.We use a least squares anamoly detection to do clustering on the time series after we get a number of records from the Tessel device. For multivariate data we could use DBSCAN. The *keys* file contains the publish, subscribe, and secret keys that are given out by Pubnub.

*climate.js* requires a 7120 climate module be attached and wifi access, as well. It writes to the PubNub channel 'hello_world'. We write a simple Json object to the wire for *eke.py* to receive. 

To get the Tessel to work with my Ubuntu 14 machine I had to do the following

    * npm install climate-si7005
    * npm install ini
    * sudo npm install pubnub
    * sudo npm install pubnub-hackathon
    * Nodejs already installed
    * sudo ln -s /usr/bin/nodejs /usr/bin/node
    * apt-get install libusb-1.0-0 libusb-1.0-0-dev
    * sudo tessel install-drivers
    * sudo tessel update
    * tessel wifi -n "pubnub-ac" -p "<pubnub-ac password>"
    * sudo npm install climate-si7020
    * sudo tessel run climate.js

[](http://mjk.freeshell.org/shiny-octo-shame.png)
