# Low Power Temperature sensor with Grafana connection using ESP32 and MicroPython

Yeah, I could probably have been able to create a better name. But, I didn't.

This will create a simple low power usage sensor (thermometer in this case) that will talk to grafana.net via an 
http call to the graphite connector.

It will be low power in the sense that the ESP32 will go into deep-sleep mode between each measurement. The
assumption is that there is a long time between each measurement (minutes-hours) that we can run the ESP32 on
a battery for a long(er) time.

The code is MicroPython, using standard libraries but also the repo micropythonexamples, where I have a few of the 
standard codesnippets required for this project.

To make this easy to work with and test on any devkit ESP32 board, the internal temperature sensor of the ESP32 is used.
Additional sensors may be added in the future.
