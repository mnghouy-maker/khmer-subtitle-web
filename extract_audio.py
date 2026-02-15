import ffmpeg

def extract_audio(video_path, audio_path):
    """
    Extract audio from video as mono 16kHz WAV
    """
    (
        ffmpeg
        .input(video_path)
        .output(audio_path, ac=1, ar=16000)
        .overwrite_output()
        .run(quiet=True)
    )
