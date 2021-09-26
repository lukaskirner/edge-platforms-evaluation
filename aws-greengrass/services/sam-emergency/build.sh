#!/bin/sh
sam build --use-container
docker run -v `pwd`/.aws-sam/build/GGCEmergencyFunction:/home python:3.8.11 pip3 install awsiotsdk -t /home
rm `pwd`/.aws-sam/build/GGCEmergencyFunction/_awscrt.cpython-38-x86_64-linux-gnu.so
