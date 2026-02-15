import streamlit as st
import os
import whisper
import ffmpeg
from deep_translator import GoogleTranslator
import tempfile

# --- PAGE CONFIG ---
st.set_page_config(page_title="Khmer Subtitle Generator", page_icon="🎬")

st.title("🎬 Video → Khmer Subtitles 🇰🇭")
st.write("Upload a video. Wait for AI processing. Download your .srt file.")

# --- HELPER FUNCTIONS ---

def extract_audio(video_path, audio_path):
    """Extracts audio from video using FFmpeg."""
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        ffmpeg.input(video_path).output(audio_path, acodec='pcm_s16le', ac=1, ar='16k').run(quiet=True)
        return True
    except Exception as e:
        st.error(f"Error extracting audio: {e}")
        return False

def format_time(seconds):
    """Converts seconds to SRT time format: HH:MM:SS,mmm"""
    td = float(seconds)
    hours = int(td // 3600)
    minutes = int((td % 3600) // 60)
    secs = int(td % 60)
    millis = int((td % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# --- MAIN APP LOGIC ---

uploaded_file = st.file_uploader("Drop video here", type=['mp4', 'mkv', 'avi', 'mov'])

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(uploaded_file.read())
        video_path = tmp_video.name

    if st.button("Start Generating Subtitles"):
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            # 1. Extract Audio
            status_text.text("Step 1/3: Extracting audio from video...")
            audio_path = video_path.replace(".mp4", ".wav")
            if extract_audio(video_path, audio_path):
                progress_bar.progress(30)

                # 2. Transcribe with Whisper (TINY model for Render)
                status_text.text("Step 2/3: AI Transcribing (this may take a few minutes)...")
                # Loading 'tiny' to stay within 512MB RAM limit
                model = whisper.load_model("tiny")
                result = model.transcribe(audio_path)
                progress_bar.progress(70)

                # 3. Translate and Generate SRT
                status_text.text("Step 3/3: Translating to Khmer...")
                translator = GoogleTranslator(source='auto', target='km')
                
                srt_content = ""
                for i, segment in enumerate(result['segments']):
                    start = format_time(segment['start'])
                    end = format_time(segment['end'])
                    text = segment['text']
                    
                    # Translate to Khmer
                    translated_text = translator.translate(text)
                    
                    srt_content += f"{i + 1}\n{start} --> {end}\n{translated_text}\n\n"
                
                progress_bar.progress(100)
                status_text.text("✅ Complete!")

                # --- THE DOWNLOAD BUTTON ---
                st.success("Your Khmer subtitles are ready!")
                st.download_button(
                    label="📥 Download Khmer Subtitles (.srt)",
                    data=srt_content,
                    file_name=f"{uploaded_file.name}_Khmer.srt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Cleanup temp files
            if os.path.exists(video_path): os.remove(video_path)
            if 'audio_path' in locals() and os.path.exists(audio_path): os.remove(audio_path)
