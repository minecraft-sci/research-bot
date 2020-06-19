#!/bin/bash

while true
do
git pull origin master
pip install -r requirements.txt
python3 bot.py
done