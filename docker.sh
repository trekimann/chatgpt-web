#!/bin/bash

if [[ $1 == "localImage" ]]; then
    docker build -t trekimann/chat-gpt-web . \
    && docker tag trekimann/chat-gpt-web 192.168.0.189:5000/chat-gpt-web \
    && docker push 192.168.0.189:5000/chat-gpt-web
else
    echo "Invalid argument. Please provide 'localImage' as an argument."
    exit 1
fi