#!/bin/bash

ps -ef | grep mongo_graph | grep -v start | awk '{print $2}' | xargs kill

nohup /usr/bin/python ./mongo_graph.py > ./mongographs.log

ps -ef | grep mongo_graph
