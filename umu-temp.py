#!/usr/bin/env python3

import urllib.request
import html
import xml.etree.ElementTree as etree
from subprocess import call

URL = "http://www8.tfe.umu.se/WeatherWebService2012/Service.asmx/Aktuellavarden"
ICON = '/Library/Widgets/Weather.wdgt/Icon.icns'

res = urllib.request.urlopen(URL)
xmlbytes = res.read()

xml = xmlbytes.decode('utf-8')
xml = html.unescape(xml)

root = etree.fromstring(xml)

temp = root[0][1].text.lstrip()
wind = root[0][4].text.lstrip()
wind_d = root[0][8].text.lstrip()
tempstr = temp + " °C"
windstr = wind_d + " (" + wind + " m/s)"

call(["growlnotify", "-n Temperatur", "-t", tempstr, "-m", windstr])
