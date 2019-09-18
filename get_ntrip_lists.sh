#!/bin/bash
#
# $Id$
# Purpose: Start ntripclient

# change these 3 according to your needs
User='gnss'
Password='gnss'
Host='gnssdata.or.kr'
Port='2101'

./ntripclient -s $Host -r $Port -u $User -p $Password

