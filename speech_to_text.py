import whisper

# Load model once
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    """
    Convert speech to text with timestamps
    """
    result = model.transcribe(audio_path)
    return result["segments"]
