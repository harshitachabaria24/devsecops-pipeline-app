#!/bin/bash
cd /home/ec2-user/app
pkill -f 'devsecops-app' || true
nohup java -jar devsecops-app-1.0-SNAPSHOT.jar > app.log 2>&1 &
