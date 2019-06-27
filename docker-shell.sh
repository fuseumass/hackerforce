docker exec -it `docker ps --format '{{.ID}}' -f 'ancestor=hacker-force'` /bin/bash
