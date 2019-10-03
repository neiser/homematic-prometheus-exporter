# Homematic Prometheus Exporter

Homematic Prometheus Exporter which scrapes for data points hardcoded in the script and exports them as Prometheus metrics. 
The data is obtained using the XML API Addon for Homematic CCU. Tested with debmatic.

## Install 

```bash
apt-get install python3-venv virtualenv

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```