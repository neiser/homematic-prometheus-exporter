import os
import time
import xml.etree.ElementTree as ET

import requests
from prometheus_client import start_http_server, PLATFORM_COLLECTOR, PROCESS_COLLECTOR, GC_COLLECTOR
from prometheus_client.core import GaugeMetricFamily, REGISTRY

MAP_METRICS = {
    '1.ACTUAL_TEMPERATURE': {'name': 'current_temperature_celsius'},
    '1.SET_POINT_TEMPERATURE': {'name': 'set_temperature_celsius'},
    '1.HUMIDITY': {'name': 'humidity_percent'},
    '10.STATE': {'name': 'heating_valve_open', 'type':'boolean'}
}

def parse_value(value, type):
    if type == 'boolean':
        if value == 'true':
            return 1
        elif value == 'false':
            return 0
        else:
            raise ValueError("Cannot parse '{}' to boolean value".format(value))
    else:
        return value


def collect_metrics_from_homematic():
    r = requests.get(url = 'http://{}/addons/xmlapi/statelist.cgi'.format(os.environ['HOMEMATIC_HOST']))
    r.raise_for_status()
    root = ET.fromstring(r.text)
    for device in root:
        room_name = device.attrib.get('name')
        for channel in device:
            for data_point in channel:
                if data_point.tag != 'datapoint':
                    continue
                data_point_name = data_point.attrib.get('name')
                data_point_type = data_point_name[data_point_name.rindex(':')+1:]
                metric = MAP_METRICS.get(data_point_type)
                if metric is not None:
                    value = parse_value(data_point.get('value'), metric.get('type'))
                    g = GaugeMetricFamily('homematic_' + metric['name'], "", labels=['room'])
                    g.add_metric([room_name], value, data_point.attrib.get('timestamp'))
                    yield g


class CustomCollector(object):
    def collect(self):
        return list(collect_metrics_from_homematic())


if __name__ == "__main__":
    for c in [PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR]:
        REGISTRY.unregister(c)
    REGISTRY.register(CustomCollector())
    start_http_server(8001)
    print("Running...")
    while True:
        time.sleep(100)
