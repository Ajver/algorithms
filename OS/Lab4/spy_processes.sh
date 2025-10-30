#!/bin/bash

# 1.
ps -eo pid,state,ppid,comm
ps -o pid,state,ppid,comm -p <pid>
kill -9 <pid>

# 2.
pstree -p

# 3.
htop
