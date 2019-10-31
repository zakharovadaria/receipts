#!/bin/sh

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -m|--message)
    MESSAGE="$2"
    shift
    shift
    ;;
    *)
    POSITIONAL+=("$1")
    shift
    ;;
esac
done
set -- "${POSITIONAL[@]}"

if [ "${MESSAGE}" = "" ]
then
  echo "Usage: $0 <message is required>"
  exit
fi

TIMESTAMP=$(date  "+%Y%m%d%H%M%S")

alembic revision --autogenerate -m "$MESSAGE" --rev-id $TIMESTAMP
