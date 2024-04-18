#!/bin/bash

set -ex

# exec python3 ./app/two_step_verification.py &
exec python3 ./app/scheduler_client.py


exec "$@"