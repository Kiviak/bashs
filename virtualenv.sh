#!/bin/bash
# install Python virtualenv for AWS Ubuntu 18.04

sudo apt update
sudo apt install python3-pip
pip3 install virtualenv
echo 'PATH=$PATH:~/.local/bin' >>.bashrc
source ~/.bashrc
virtualenv venv
source ~/venv/bin/activate
pip install supervisor
echo_supervisord_conf > ~/supervisord.conf
pip list
