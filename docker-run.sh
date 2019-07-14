#!/bin/bash
docker run -v `pwd`:/app -p 8080:8080 -it hacker-force "$@"
