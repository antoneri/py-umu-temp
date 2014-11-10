#!/usr/bin/env python3
from urllib.request import urlopen
from html import unescape
import xml.etree.ElementTree as ET

URL = "http://www8.tfe.umu.se/WeatherWebService2012/Service.asmx/Aktuellavarden"
NS = "{http://tempuri.org/}"

def fetch_data():
    try:
        src = urlopen(URL).read().decode('utf-8')
    except Exception as e:
        print("Error: Something went wrong fetching the page: {}".format(e))
        return None

    xml = unescape(src)
    root = ET.fromstring(xml)[0]

    def tag_contents(tag):
        try:
            return root.find("{}{}".format(NS, tag)).text.strip()
        except Exception as e:
            print("Error: Could not find tag {}.".format(tag))
            return None

    temp = tag_contents("tempmed")
    speed = tag_contents("vindh")
    words = tag_contents("vindord")

    temp = "{} °C".format(temp)
    speed = "{} m/s".format(speed)
    return temp, speed, words


def main():
    import os
    temp, speed, words = fetch_data()

    script = ('display notification "{} ({})"'
                ' with title "Temperatur"'
                ' subtitle "{}"').format(words, speed, temp)

    os.system("osascript -e '{}'".format(script))


if __name__ == '__main__':
    main()
