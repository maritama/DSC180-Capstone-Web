#!/bin/bash
cd /app/phrase-mining
python3 run.py

cp -a /app/phrase-mining/data/outputs/. /usr/local/tomcat/webapps/python/img/
