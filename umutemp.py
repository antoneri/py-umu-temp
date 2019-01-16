#!/usr/local/bin/python3
import sys
from urllib.request import urlopen
from html import unescape
from xml.etree import ElementTree


def fetch_data():
    api_url = "http://www8.tfe.umu.se/WeatherWebService2012/Service.asmx/Aktuellavarden"
    namespace = "{http://tempuri.org/}"

    try:
        src = urlopen(api_url).read().decode('utf-8')
    except Exception as e:
        sys.exit("Could not connect to server. {}".format(e))

    xml = unescape(src)
    root = ElementTree.fromstring(xml)[0]

    temp, speed, words = [root.find(namespace + tag).text.strip() for tag in ("tempmed", "vindh", "vindord")]

    temp = "{} °C".format(temp)
    speed = "{} m/s".format(speed)
    return temp, speed, words


def main(notifier):
    import os
    temp, speed, words = fetch_data()

    if notifier == "growl":
        icon = "/Library/Widgets/Weather.wdgt/Icon.icns"
        os.system(('growlnotify -n "Temperatur"'
                   ' -m "Temperatur {}\n{} ({})"'
                   ' --image "{}"').format(temp, words, speed, icon))

    elif notifier == "osx":
        script = ('display notification "{} ({})"'
                  ' with title "Temperatur {}"').format(words, speed, temp)
        os.system("osascript -e '{}'".format(script))

    elif notifier == "echo":
        sys.exit("{}, {} ({})".format(temp, words, speed))

    elif notifier == "bitbar":
        print(temp)
        print("---")
        print("{} ({})".format(words, speed))
        print("TFE väder | href=http://www8.tfe.umu.se/weather-new/")

    else:
        sys.exit("Unhandled notifier.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        main("bitbar")
    else:
        main(sys.argv[1])
