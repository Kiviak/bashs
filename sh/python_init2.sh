#!/bin/bash
# Use venv to create virtual environments

sudo apt update
sudo apt install python3-pip && echo 'PATH=$PATH:~/.local/bin' >> ~/.bashrc \
                            && source ~/.bashrc \
                            && python3 -m venv ~/venv && source ~/venv/bin/activate \
                            && pip install supervisor \
                            && echo_supervisord_conf > ~/supervisord.conf \
                            && pip list
