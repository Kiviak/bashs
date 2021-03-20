#!/bin/bash

curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh > ~/v2ray-install.sh
chmod +x ~/v2ray-install.sh
sudo ~/v2ray-install.sh
git clone git@github.com:Kiviak/hotdata.git ~/hotdata
v2ray -c ~/hotdata/v2ray-server.json 
