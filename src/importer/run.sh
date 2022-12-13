#!/bin/bash

if [ $USE_DEV_MODE = "true" ];
  then nodemon main.py;
  else python main.py;
fi