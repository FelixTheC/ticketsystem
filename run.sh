#!/usr/bin/env bash
docker run -t -i -h Ticketsystem --restart=always --name Ticketsystem -d -p 9004:8000 -v /DockerRepository/Ticketsystem/ticketsystem:/ticketsystem ticketsystem
