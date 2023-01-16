import sounddevice as sd
import soundfile as sf
import customtkinter
import tkinter as tk
from tkinter import filedialog as fd 
import whisper 
import pyperclip

## Globals
recording = False
WHISPER_CONFIG = {'model': 'base', 'file_name': 'scratch_audio.flac', 'task':'transcribe', 'detectedLanguage': '', 'text': ''}
UI_CONFIG = {'flacDescription':'Flac audio files', 'default': 'Press start or pick a file to begin transcription', 'busy': '📝 Transcribing...', 'done':'✅ Job finished', 'done:recording':'🎤 Recording done', 'start':'▶ Start', 'stop': '■ Stop', 'clear':'✖ Clear', 'load': '📁 Load Audio from File', 'transcribe': '📝 Transcribe', 'keeptalking': 'Keep talking for 10 seconds', 'loadingmodel': '🛰 Loading model...', 'dark_mode':False }

app = customtkinter.CTk()
app.title("Whisper POC")
MODEL_OPTIONS = ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large']
selectedModelVar = tk.StringVar(app)

# Set mode
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"

root_frame = customtkinter.CTkFrame(master=app)
root_frame.pack(pady=20, padx=20, fill="both", expand=True)

def updateLabel(text):
    rootLabel.configure(text=text)
    recordButton.update()

def updateTranscription(text):
    transcribeBox.delete("1.0", tk.END)
    transcribeBox.insert("1.0", text)
    transcribeBox.update()

def updateButton(text):
    recordButton.configure(text=text)
    recordButton.update()

def clear_text():
    transcribeBox.delete("1.0", tk.END)
    transcribeBox.update()


def start_recording():
    global recording
    updateButton(UI_CONFIG["stop"])
    clear_text()
    if not recording:
        recording = True
        fs = 48000 
        duration = 10
        updateLabel(UI_CONFIG["keeptalking"])
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        sf.write(WHISPER_CONFIG["file_name"], myrecording, fs)
        updateLabel(UI_CONFIG["done:recording"])
        
        # Reset record button
        updateButton(UI_CONFIG["start"])
        recording = False

        transcribeButton.configure(state = 'active')
    else:
        updateLabel(UI_CONFIG["default"])
        updateButton("▶ Start")
        recording = False

def transcribe():
   
    clear_text()
    updateLabel(UI_CONFIG["loadingmodel"])
   
    model = whisper.load_model(WHISPER_CONFIG["model"])
    language = "en" if WHISPER_CONFIG["model"].endswith(".en") else None
    audio = WHISPER_CONFIG["file_name"]
    options = {"fp16": False, "language": language, "task": WHISPER_CONFIG["task"]}
   
    # Transcribe (could also be translate)
    results = model.transcribe(audio, **options)
   
    transcribe_text = results["text"] + "\n"
    WHISPER_CONFIG["detectedLanguage"] = results["language"]
    WHISPER_CONFIG["text"] = results["text"]
   
    #debug
    print("")
    print(WHISPER_CONFIG)
    print("")

    updateTranscription(transcribe_text)
    updateLabel(UI_CONFIG["done"])

def reset():
    updateLabel(UI_CONFIG['default'])
    clear_text()

def copy_to_clipboard():
    text = transcribeBox.get("1.0", tk.END)
    pyperclip.copy(text)

# rest of the UI code
rootLabel = tk.Label(master=root_frame, justify=tk.LEFT, text=UI_CONFIG["default"])
rootLabel.pack(pady=10, padx=10)

menu = customtkinter.CTkComboBox(root_frame, variable=selectedModelVar,values=MODEL_OPTIONS)
menu.pack(pady=10, padx=10)

recordButton = tk.Button(master=root_frame,text=UI_CONFIG["start"],command=start_recording)
recordButton.pack(pady=5, padx=10)

transcribeButton = tk.Button(master=root_frame, text="📝 Transcribe", command=transcribe, state = "disabled")
transcribeButton.pack(pady=10, padx=10)


def loadFile():
    fileName = fd.askopenfilename(filetypes=[(UI_CONFIG["flacDescription"], "*.flac")])
    print(fileName)
    if fileName != '':
        WHISPER_CONFIG["file_name"] = fileName
        transcribe()

fileButton = tk.Button(master=root_frame, text=UI_CONFIG["load"], command=loadFile)
fileButton.pack(pady=10, padx=10)

transcribeBox = customtkinter.CTkTextbox(master=root_frame, width=300)
transcribeBox.pack(pady=10, padx=10)
transcribeBox.insert("0.0", "")

copyButton = tk.Button(master=root_frame, text="© Copy!", command=copy_to_clipboard)
copyButton.pack(pady=10, padx=10)

clearButton = tk.Button(master=root_frame, text=UI_CONFIG["clear"], command=reset)
clearButton.pack(pady=10, padx=10)


## Set starting model
BASE_MODEL = MODEL_OPTIONS[3]
selectedModelVar.set(BASE_MODEL)
menu.set(BASE_MODEL)
WHISPER_CONFIG["model"] = BASE_MODEL

# parser = argparse.ArgumentParser(description='Yay.')
# args = parser.parse_args()
# # if there is text in args
# # if there is 
# print(args.accumulate(args.integers))

app.mainloop()

