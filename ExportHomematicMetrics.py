import xml.etree.ElementTree as ET

import requests

MAP_METRICS = {
    '1.ACTUAL_TEMPERATURE': {'name': 'current_temperature_celsius'},
    '1.SET_POINT_TEMPERATURE': {'name': 'set_temperature_celsius'},
    '1.HUMIDITY': {'name': 'humidity_percent'},
    '10.STATE': {'name': 'heating_valve_open', 'type':'boolean'}
}

r = requests.get(url = 'http://homematic/addons/xmlapi/statelist.cgi')
r.raise_for_status()

root = ET.fromstring(r.text)

for device in root:
    room_name = device.attrib.get('name')
    print("Device '{}'".format(room_name))
    for channel in device:
        for data_point in channel:
            if data_point.tag != 'datapoint':
                continue
            data_point_name = data_point.attrib.get('name')
            data_point_type = data_point_name[data_point_name.rindex(':')+1:]
            metric = MAP_METRICS.get(data_point_type)
            if metric is not None:
                print("Metric {} has value {}".format(metric['name'], data_point.get('value')))