#!/usr/bin/env python3
import sys
from urllib.request import urlopen
from html import unescape
import xml.etree.ElementTree as ET

URL = "http://www8.tfe.umu.se/WeatherWebService2012/Service.asmx/Aktuellavarden"
NS = "{http://tempuri.org/}"
DEFAULT = "growl"

def fetch_data():
    src = urlopen(URL).read().decode('utf-8')
    xml = unescape(src)
    root = ET.fromstring(xml)[0]

    tag_contents = lambda tag: root.find(NS + tag).text.strip()
    temp, speed, words = map(tag_contents, ["tempmed", "vindh", "vindord"])

    temp = "{} °C".format(temp)
    speed = "{} m/s".format(speed)
    return temp, speed, words


def main(notifier):
    import os
    temp, speed, words = fetch_data()

    if notifier == "growl":
        icon = "/Library/Widgets/Weather.wdgt/Icon.icns"
        command = ('growlnotify -n "Temperatur"'
                   ' -m "Temperatur {}\n{} ({})"'
                   ' --image "{}"').format(temp, words, speed, icon)

    elif notifier == "osx":
        script = ('display notification "{} ({})"'
                  ' with title "Temperatur"'
                  ' subtitle "{}"').format(words, speed, temp)
        command = "osascript -e '{}'".format(script)

    else:
        sys.exit("Unhandled notifier. Exiting...")

    return os.system(command)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        main(DEFAULT)
    else:
        main(sys.argv[1])

