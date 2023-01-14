import argparse
import whisper 
import sounddevice as sd
import soundfile as sf

# globals
debug = False

# default configuration for whisper
WHISPER_CONFIG = {
    'model': 'base', 
    'default:file_name':'scratch_audio.flac',
    'file_name': '', 
    'task':'transcribe', 
    'detectedLanguage': '', 
    'text': ''
}

def loud(message):
    """Prints message to console if in debug mode"""
    if debug == True:
        print("")
        print("#########################")
        print(message)
        print("#########################")
        print("")

def start_recording(duration=10, file_name=WHISPER_CONFIG["default:file_name"]):
    """Records audio using sounddevice library and saves it to specified file"""
    loud("Begin speaking for " + duration + " seconds")
    fs = 48000 
    myrecording = sd.rec(int(int(duration) * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(file_name, myrecording, fs)
    loud('Recording complete')

def transcribe(file_name=WHISPER_CONFIG["file_name"], model_name=WHISPER_CONFIG["model"], language=None, task='transcribe'):
    """Transcribes audio file using whisper library"""
    model = whisper.load_model(model_name)
    options = {"fp16": False, "language": language, "task": task}
    if task == 'translate':
        results = model.transcribe(file_name, **options)
    else:
        results = model.transcribe(file_name, **options)
    WHISPER_CONFIG["detectedLanguage"] = results["language"]
    WHISPER_CONFIG["text"] = results["text"]
    loud(WHISPER_CONFIG)
    print(results["text"])
    return transcribe

# CLI Stuff
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")

# Add new arguments
parser.add_argument("--file", help="file path for audio to transcribe")
parser.add_argument("--model", help="model to use for transcription", default="base")
parser.add_argument("--language", help="language of audio to transcribe", default=None)
parser.add_argument("--task", help="transcription task (transcribe or translate)", default='transcribe')
parser.add_argument("--record", help="flag to start recording audio", action="store_true")
parser.add_argument("--duration", help="duration of recording in seconds", default=10)

args = parser.parse_args()
if args.verbose:
    debug = True

# Handle CLI cases
selectedLanguage = None
if args.language == None:
    if args.model.endswith(".en"):
        selectedLanguage = "en"

if args.record:
    start_recording(duration=args.duration)
    file_name = WHISPER_CONFIG["default:file_name"]
elif args.file:
    file_name = args.file
else:
    file_name = WHISPER_CONFIG["file_name"]

transcribe(file_name=file_name, model_name=args.model, language=selectedLanguage, task=args.task)
