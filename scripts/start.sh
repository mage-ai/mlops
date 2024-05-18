#!/bin/bash

MAGE_CODE_PATH=/home/mage_code \
  PROJECT_NAME=mlops \
  SMTP_EMAIL=$SMTP_EMAIL \
  SMTP_PASSWORD=$SMTP_PASSWORD \
  docker compose up
