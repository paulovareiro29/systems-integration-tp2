#!/bin/bash

if [ $USE_DEV_MODE = "true" ];
  then nodemon main.py $RPC_SERVER_PORT;
  else python main.py $RPC_SERVER_PORT;
fi