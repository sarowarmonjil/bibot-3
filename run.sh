#!/usr/bin/env bash
# fuck the crontab
env | sed 's/^\([^=]*\)=\(.*\)$/\1="\2"/g' > src/envs.py
supervisord --nodaemon
