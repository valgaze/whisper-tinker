#!/bin/bash

# Get current shell
current_shell=$(echo $SHELL | awk -F/ '{print $NF}')

# Initialize conda
if [ "$current_shell" == "bash" ]; then
    conda init bash
else
    conda init $current_shell
fi
conda deactivate && conda env remove -n whisper_app