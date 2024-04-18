#!/bin/bash

set -ex

# exec python3 multiple_frame_creation.py &
exec python3 ./app/run_multiple_scheduler_client.py 


exec "$@"