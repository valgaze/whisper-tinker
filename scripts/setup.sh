#!/bin/bash

# Get current shell
current_shell=$(echo $SHELL | awk -F/ '{print $NF}')

# Initialize conda
if [ "$current_shell" == "bash" ]; then
    conda init bash
else
    conda init $current_shell
fi

# create whisper_app
conda create --name whisper_app python=3.9 -y

# Activate whisper_app environment
conda activate whisper_app

# Install pip
conda install pip

# Install Whisper
pip install git+https://github.com/openai/whisper.git

# Install UI tooling
pip install tk customtkinter

# Install recording and write-to-file utilities
pip install sounddevice soundfile

echo "SETUP COMPLETE"
