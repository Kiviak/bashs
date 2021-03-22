#!/bin/bash

curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh > ~/v2ray-install.sh
chmod +x ~/v2ray-install.sh
sudo ~/v2ray-install.sh
FILE=~/hotdata/v2ray/v2ray-server.json
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    git clone git@github.com:Kiviak/hotdata.git ~/hotdata
fi
v2ray -c $FILE
