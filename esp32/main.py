# Very simple example of how to use request to get a web page
# If web page responds with status code 200 (OK) then blue LED is turned on.

import wlan
import urequests
import time

if __name__ == "__main__":
    wlan.do_connect()

    while(1):
        response = urequests.get('https://example.com')
        status = response.status_code
