import tkinter as tk
import customtkinter as ctk
import soundfile as sf
import sounddevice as sd
import whisper # pip install git+https://github.com/openai/whisper.git

# WHISPER CONFIG
# model types: tiny", "base", "small", "medium", "large" 
# Task types: "transcribe", "translate" 
# https://github.com/openai/whisper#available-models-and-languages

WHISPER_CONFIG = {'model': 'base', 'file_name': 'scratch_audio.flac', 'task':'transcribe'}

# Text labels
UI_CONFIG = {'default': 'Press Record', 'busy': 'Working...', 'done': 'Done!'}


# Select from the following models: "tiny", "base", "small", "medium", "large"
model = whisper.load_model(WHISPER_CONFIG["model"])

# create the app
app = tk.Tk()
app.geometry("500x600")
app.title("Whisper POC")
root_frame = ctk.CTkFrame(master=app)
root_frame.pack(pady=20, padx=60, fill="both", expand=True)



def updateLabel(text):
    rootLabel.configure(text=text)

def updateTranscription(text):
    transcribeLabel.configure(text=text)

def voice_rec():
    updateLabel(UI_CONFIG["done"])
    fs = 48000 # frequency sampling (see https://github.com/sudo-Boris/whisperapp/blob/main/v1/app.py#L25)
    duration = 10
    updateLabel(text="Keep talking for 10 seconds")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(WHISPER_CONFIG["file_name"], myrecording, fs)
    updateLabel(UI_CONFIG["done"])

def transcribe():
    updateLabel("busy...")
    audio = WHISPER_CONFIG["file_name"]
    options = {"fp16": False, "language": None, "task": WHISPER_CONFIG["task"]}
    results = model.transcribe(audio, **options)
    print('TRANSCRIPTION', results["text"])
    updateLabel(text=UI_CONFIG["default"])
    transcribeLabel.insert("0.0", results["text"])



rootLabel = ctk.CTkLabel(master=root_frame, justify=tk.LEFT, text=UI_CONFIG["default"])
rootLabel.pack(pady=10, padx=10)

recordButton = ctk.CTkButton(master=root_frame,text="🎤 Record",height=40,width=120,command=voice_rec)
recordButton.pack(pady=10, padx=10)

transcribeButton = ctk.CTkButton(master=root_frame, height=40,width=120, text="📝 Transcribe", command=transcribe)
transcribeButton.pack(pady=10, padx=10)

transcribeLabel = ctk.CTkTextbox(master=root_frame, width=300, height=150)
transcribeLabel.pack(pady=10, padx=10)
transcribeLabel.insert("0.0", "")


# run app
app.mainloop()