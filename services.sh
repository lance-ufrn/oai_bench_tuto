#!/bin/bash

set -e

dockerCmd="docker compose"
if (( $# == 2 )); then
    dockerCmd="docker-compose"
fi

if (( $# < 1 )); then
    echo "Illegal number of parameters"
    echo "usage: services [ n106 = PRB106 USRP n310 | n162 = PRB162 USRP n310 | n273 = PRB273 USRP n310 | b106 = PRB106 USRP b210 | b162 = PRB162 USRP b210 | stop ]"

    exit 1
fi



command="$1"
case "${command}" in
	"help")
		echo "usage: services [ n106 = PRB106 USRP n310 | n162 = PRB162 USRP n310 | n273 = PRB273 USRP n310 | b106 = PRB106 USRP b210 | b162 = PRB162 USRP b210 | stop ]"
		;;
	"n106")
		${dockerCmd} -f docker-compose/docker-compose-n310-PRB106.yaml up 
		;;
	"n162")
		${dockerCmd} -f docker-compose/docker-compose-n310-PRB162.yaml up
		;;
        "n273")
                ${dockerCmd} -f docker-compose/docker-compose-n310-PRB273.yaml up
                ;;
        "b106")
                ${dockerCmd} -f docker-compose/docker-compose-b210-PRB106.yaml up
                ;;
        "b162")
                ${dockerCmd} -f docker-compose/docker-compose-b210-PRB162.yaml up
                ;;
        "stop")
                sudo docker stop $(sudo docker ps -a -q)
                ;;
       	*)
		echo " Command not Found."
		echo "usage: services [ n106 = PRB106 USRP n310 | n162 = PRB162 USRP n310 | n273 = PRB273 USRP n310 | b106 = PRB106 USRP b210 | b162 = PRB162 USRP b210 | stop ]"
		exit 127;
		;;
esac
