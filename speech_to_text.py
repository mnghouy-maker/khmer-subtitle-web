import whisper

def transcribe_audio(path):
    # 'tiny' is the only version that reliably fits in 512MB RAM
    model = whisper.load_model("tiny") 
    result = model.transcribe(path)
    return result["segments"]
