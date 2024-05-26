#!/usr/bin/env python

import datetime
import psutil
import socket
from influxdb import InfluxDBClient

ifuser = "influx_user"
ifpass = "influx_password"
ifdb   = "influx_db"
ifhost = "influx_host"
ifport = 9001

net = ('eth0')
drive =('/')
#sensor = ('coretemp')
sensor = ('cpu_thermal')

hostname = socket.gethostname()
time = datetime.datetime.utcnow()

cpu = psutil.cpu_percent(interval=1)
disk = psutil.disk_usage(drive)
mem = psutil.virtual_memory()
load = psutil.getloadavg()
temp = (psutil.sensors_temperatures().get(sensor)[0][1])
bsend = (psutil.net_io_counters(pernic=True).get(net)[0])
breceived = (psutil.net_io_counters(pernic=True).get(net)[1])

data = [
    {
        "measurement": hostname,
        "time": time,
        "fields": {
            "cpu": cpu,
            "load_1": load[0],
            "load_5": load[1],
            "load_15": load[2],
            "disk_percent": disk.percent,
            "disk_free": disk.free,
            "disk_used": disk.used,
            "mem_percent": mem.percent,
            "mem_free": mem.free,
            "mem_used": mem.used,
            "temp": temp,
            "bsend": bsend,
            "breceived": breceived
        }
    }
]

print(data)

ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
ifclient.write_points(data)

