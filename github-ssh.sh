#!/bin/bash
#add a new ssh key to github
echo "github ssh key: start..."
echo "Enter your GitHub email address: "  
read user_email
ssh-keygen -t ed25519 -C $user_email
eval `ssh-agent -s`
ssh-add ~/.ssh/id_ed25519
echo "your ssh public key is below,add it to your account:"
cat ~/.ssh/id_ed25519.pub
KEY=$(cat ~/.ssh/id_ed25519.pub)
echo "input the name of the ssh key:"
read TITLE
JSON=$( printf '{"title": "%s", "key": "%s"}' "$TITLE" "$KEY" )
FILE=~/hotdata/github/token
if [ -f "$FILE" ]; then
    echo "$FILE exists."
    TOKEN=$(cat $FILE)
else 
    echo "input your github token:"
    read TOKEN
fi
curl -X POST \
         -H "Accept: application/vnd.github.v3+json" \
         -H "Authorization: token $TOKEN" \
         -d "$JSON" \
        "https://api.github.com/user/keys?access_token=$TOKEN"