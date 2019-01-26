#!/usr/bin/env bash
set -e
set -x

ssh jacek@localhost -p 8093 "mkdir /home/jacek/Desktop/promMetricsService || true"
scp -P 8093 /var/lib/jenkins/workspace/promServiceMetrics\ deploy/serviceViews.py jacek@localhost:/home/jacek/Desktop/promMetricsService/serviceViews.py
scp -P 8093 /var/lib/jenkins/workspace/promServiceMetrics\ deploy/pan-tadeusz.txt jacek@localhost:/home/jacek/Desktop/promMetricsService/pan-tadeusz.txt
ssh jacek@localhost -p 8093 "pip3 install flask"
ssh jacek@localhost -p 8093 "pip3 install prometheus_client"
ssh jacek@localhost -p 8093 "screen -X -S promMetricsService quit || true"
ssh jacek@localhost -p 8093 "screen -d -m -S promMetricsService bash -c 'python3 /home/jacek/Desktop/promMetricsService/serviceViews.py /home/jacek/Desktop/promMetricsService/pan-tadeusz.txt'"

