#!/bin/bash

#source ~/dsa/autoanki/virenv/bin/activate
#python3 ~/dsa/autoanki/ankimake.py "./cards.txt"
tmux neww bash -c "source ~/dsa/autoanki/virenv/bin/activate;python3 ~/dsa/autoanki/ankimake.py '/home/pesi/dsa/autoanki/cards.txt';read -n 1 -s -r -p 'press any key to continue'"
