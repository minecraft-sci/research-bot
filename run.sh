#!/bin/bash

while true
do
git pull origin master
pip3 install -r requirements.txt
python3 bot.py
done