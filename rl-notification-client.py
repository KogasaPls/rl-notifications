#!/usr/bin/env pypy3

import socket
import os

user = os.environ.get('DUNST_SUMMARY').replace("RuneLite - ", "", 1)
message = os.environ.get('DUNST_BODY')
byteString = user + ' ' + message

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.connect("/tmp/rl-notification")
    client.send(byteString.encode('utf-8'))
    client.close()
