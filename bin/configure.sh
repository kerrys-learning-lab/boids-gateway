#! /bin/bash
curl  -X POST \
      -H "Content-type: application/json" \
      -d@/opt/boids-gateway/bin/configure.json \
      http://localhost:8888/api/v1/session
