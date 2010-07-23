#!/bin/bash

ps -ef | grep mongo_graph | grep -v start | awk '{print $2}' | xargs kill

nohup /usr/bin/python /home/kgorman/mongographs/mongo_graph.py > /home/kgorman/mongographs/mongographs.log

ps -ef | grep mongo_graph
