var pubnub = require("pubnub-hackathon").init({publish_key: "pub-e1b117e4-5f92-423e-b238-edf1f016949a", subscribe_key: "sub-e647e14a-1624-11e2-9589-937edcd48fdd"});
var tessel = require('tessel');
var climatelib = require('climate-si7020');
var climate = climatelib.use(tessel.port['A']);


//pubnub.init({publish_key: "pub-e1b117e4-5f92-423e-b238-edf1f016949a", subscribe_key: "sub-e647e14a-1624-11e2-9589-937edcd48fdd"});

climate.on('ready', function(){
  setInterval(function(){
    climate.readHumidity(function(err, humid){
      climate.readTemperature('f', function(err, temp){
          //console.log('Degrees:', temp.toFixed(4) + 'F', 'Humidity:', humid.toFixed(4) + '%RH');
	  //var s = "Degrees:" +  temp.toFixed(4) + 'F' +  'Humidity:' + humid.toFixed(4) + '%RH';
	  var s = "degrees: " + temp.toFixed(4)
	  var s = {"temp": temp.toFixed(4) };
	  console.log(s)
	  pubnub.publish({channel: "hello_world", message: s})
      });
    });
  }, 1000);
});

climate.on('error', function(err) {
  console.log('error connecting module', err);
});
