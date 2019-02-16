#!/usr/bin/env bash

./stop-server.sh
rm -rf serve_scala-0.1
unzip serve_scala-0.1.zip
./start-server.sh
