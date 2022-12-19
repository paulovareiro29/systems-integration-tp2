#!/bin/bash

npm install;

rm .env
touch .env
echo "REACT_APP_API_ENTITIES_URL=$API_ENTITIES_URL" >> .env
echo "REACT_APP_API_GIS_URL=$API_GIS_URL" >> .env
echo "REACT_APP_API_GRAPHQL_URL=$API_GRAPHQL_URL" >> .env
echo "REACT_APP_API_PROC_URL=$API_PROC_URL" >> .env

if [ $USE_DEV_MODE = "true" ];
  then
    npm run start;
  else
    npm run build;
    node server $WEB_PORT;
fi