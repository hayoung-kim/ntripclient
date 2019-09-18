#!/bin/bash
#
# $Id$
# Purpose: Start ntripclient

# change these 3 according to your needs
Stream=$(cat /tmp/mountpoint)
User='gnss'
Password='gnss'
Host='gnssdata.or.kr'
Port='2101'

DateStart=`date -u '+%s'`
SleepMin=10     # Wait min sec for next reconnect try
SleepMax=10000  # Wait max sec for next reconnect try
(while true; do
  ./ntripclient -s $Host -r $Port -d $Stream -u $User -p $Password
  if test $? -eq 0; then DateStart=`date -u '+%s'`; fi
  DateCurrent=`date -u '+%s'`
  SleepTime=`echo $DateStart $DateCurrent | awk '{printf("%d",($2-$1)*0.02)}'`
  if test $SleepTime -lt $SleepMin; then SleepTime=$SleepMin; fi
  if test $SleepTime -gt $SleepMax; then SleepTime=$SleepMax; fi
  # Sleep 2 percent of outage time before next reconnect try
  sleep $SleepTime
done) 

