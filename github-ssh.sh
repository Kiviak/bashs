#!/bin/bash

echo "github ssh key: start..."
echo "Enter your GitHub email address: "  
read user_email
ssh-keygen -t ed25519 -C $user_email
eval `ssh-agent -s`
ssh-add ~/.ssh/id_ed25519
echo "your ssh public key is below,add it to your account:"
cat ~/.ssh/id_ed25519.pub