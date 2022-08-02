# Very simple example of how to use request to get a web page
# If web page responds with status code 200 (OK) then blue LED is turned on.

import wlan
import urequests
import json
import time
import ntptime
import grafanaconfig
import esp32
import machine

if __name__ == "__main__":


    wlan.do_connect()

    # Get the time
    # NOT IF RESTART
    #rtc = machine.RTC()
    ntptime.settime()
    POSIX_delta = 946684800 #ESP32 uses year 2000, linux 1970
    timestamp = time.time() + POSIX_delta
    print("Timestamp: {}".format(timestamp))

    current_temp=esp32.raw_temperature()
    print("Temperature: {}".format(current_temp))

    headers = {'content-type': 'application/json'}
    INTERVAL=60
    actualtempdict = {"name": "actual_temperature", "interval": INTERVAL, "value": current_temp, "mtype":"gauge", "time": timestamp}
    mylist=[actualtempdict]
    data = json.dumps(mylist)
    print("Sending data {}".format(data))

    #response = urequests.get('https://example.com')
    response = urequests.post(
        grafanaconfig.GRAFANA_URL,
        data=data,
        auth = (grafanaconfig.GRAFANA_USER, grafanaconfig.GRAFANA_TOKEN),
        headers=headers
    )
    status = response.status_code
    print("HTTP status code: {}".format(status))
