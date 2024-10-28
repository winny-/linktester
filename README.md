# Linktester

An experiment testing link quality using off the shelf tools.  "What if
Speedtest was a Python script that works against any host?"

## Example

### Access home NAS via fast access point

```
$ python -m linktester silo.home.winny.tech
silo.home.winny.tech (silo.winny.tech -> 10.20.0.4)
MTR PING best/avg/worst/stddev 4.38/5.68/7.66/1.2 ms
IPERF    Up/Down 548/647 Mbps
```

### Acess home NAS via older router

Whoa, that is a lot more latency and diminished bandwidth!

```
$ python -m linktester silo.home.winny.tech
silo.home.winny.tech (meet.winny.tech -> 10.20.0.4)
MTR PING best/avg/worst/stddev 0.92/39.07/84.96/35.3 ms
IPERF    Up/Down 26/62 Mbps
```


## How to use

1. Set up a host with iperf3 server and responds to ICMP Pings.
2. Run the tool: `python -m linktester yourhostwithiperf3andpings.example`

## What it can do now

Run a test.  Hangs in `iperf` coroutine if the server is unavailable.

## Vision

Linktester facilitates the measuring of latency, bandwidth, and data loss of IP
network segments.  It records annotated tests for data analysis.  It reports on
metrics from the stored test results.
