#!/usr/bin/env bash
touch main.log
# fuck the crontab
env | sed 's/^\([^=]*\)=\(.*\)$/\1="\2"/g' > src/envs.py
cron && tail -f main.log
