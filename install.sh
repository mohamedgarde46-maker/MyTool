#!/bin/bash

echo "Installing MyTool..."

sudo apt update

pip3 install -r requirements.txt

chmod +x main.py

sudo cp main.py /usr/local/bin/mytool

echo "Installation Complete."