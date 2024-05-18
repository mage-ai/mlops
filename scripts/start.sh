#!/bin/bash

MAGE_CODE_PATH=/home/src \
  PROJECT_NAME=mlops \
  SMTP_EMAIL=$SMTP_EMAIL \
  SMTP_PASSWORD=$SMTP_PASSWORD \
  docker compose up
