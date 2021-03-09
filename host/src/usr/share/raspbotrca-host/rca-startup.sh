#!/bin/bash
# description: Raspbot RCA host application service.

case "$1" in
    start)
       sudo python3 /usr/bin/raspbotrca-host-manualstart
       ;;
    stop)
       sudo pkill -9 -f /usr/share/raspbotrca-host/main.py
       ;;
    restart)
       sudo pkill -9 -f /usr/share/raspbotrca-host/main.py
       sudo python3 /usr/bin/raspbotrca-host-manualstart
       ;;
    *)
      echo "Usage: /etc/init.d/rca-startup.sh {start|stop|restart}"
esac

exit 0
