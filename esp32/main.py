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

# Time between samples in seconds
INTERVAL=600
# Blue LED
LED = machine.Pin (2, machine.Pin.OUT)


if __name__ == "__main__":

    # Turn on LED to indicate it is awake.
    LED.value(1)

    # Connect to WiFi
    wlan.do_connect()

    if machine.reset_cause() != machine.DEEPSLEEP_RESET:
        print('Power on or hard reset, set the time')
        # NTP is timing out often. This may require retries
        timeset = False
        while not timeset:
            try:
                ntptime.settime()
                timeset = True
            except:
                timeset = False
                time.sleep(1)

    POSIX_delta = 946684800 #ESP32 uses year 2000, linux 1970 for EPOCH
    timestamp = time.time() + POSIX_delta
    print("Timestamp: {}".format(timestamp))

    current_temp=esp32.raw_temperature()
    print("Temperature: {}".format(current_temp))


    # Build the strings for HTTP request
    headers = {'content-type': 'application/json'}
    actualtempdict = {"name": "actual_temperature", "interval": INTERVAL, "value": current_temp, "mtype":"gauge", "time": timestamp}
    mylist=[actualtempdict]
    data = json.dumps(mylist)
    print("Sending data {}".format(data))

    # Send http post to grafana.net
    response = urequests.post(
        grafanaconfig.GRAFANA_URL,
        data=data,
        auth = (grafanaconfig.GRAFANA_USER, grafanaconfig.GRAFANA_TOKEN),
        headers=headers
    )
    status = response.status_code
    print("HTTP status code: {}".format(status))

    # Turn off LED as we go do sleep
    LED.value(0)
    print("Going to deepsleep for {}s".format(INTERVAL))
    machine.deepsleep(INTERVAL * 1000)
