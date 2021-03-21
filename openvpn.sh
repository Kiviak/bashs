#!/bin/bash

curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
chmod +x openvpn-install.sh
sudo ./openvpn-install.sh
echo openvpn default port: 1194
echo vpn start: sudo /etc/init.d/openvpn start
