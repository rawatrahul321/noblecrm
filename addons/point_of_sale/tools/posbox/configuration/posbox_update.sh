#!/usr/bin/env bash

sudo mount -o remount,rw /
sudo git --work-tree=/home/pi/noblecrm/ --git-dir=/home/pi/noblecrm/.git pull
sudo mount -o remount,ro /
(sleep 5 && sudo reboot) &
