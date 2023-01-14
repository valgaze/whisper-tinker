# https://github.com/conda/conda/issues/7980
# https://stackoverflow.com/questions/34534513/calling-conda-source-activate-from-bash-script
eval "$(conda shell.bash hook)"

conda create --name whisper_app python=3.9 -y
conda activate whisper_app
conda install pip
pip install git+https://github.com/openai/whisper.git # Install Whisper
pip install tk customtkinter # Install UI tooling, tk + customtk
pip install sounddevice soundfile # Install recording and write-to-file
echo "Run the following to activate: conda activate whisper_app"


