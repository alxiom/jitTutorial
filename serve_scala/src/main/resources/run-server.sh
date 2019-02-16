#!/bin/bash

mkdir -p $HOME/temp

binPath=./serve_scala-0.1/bin/serve_scala

source run-server.config

${binPath} -Dlogback.configurationFile=logback-http.xml -Dport=${port} -Dinput_dim=${inputDim} -Dfile.encoding=UTF-8 -Djava.io.tmpdir=/home1/irteam/temp -J-Xms${memory}G -J-Xmx${memory}G -J-XX:+UseG1GC -J-server
