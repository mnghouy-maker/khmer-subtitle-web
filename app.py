import streamlit as st
import os
import tempfile

from extract_audio import extract_audio
from speech_to_text import transcribe_audio
from translate_khmer import translate_to_khmer
from srt_generator import generate_srt

st.set_page_config(
    page_title="Video → Khmer Subtitle",
    layout="centered"
)

st.title("🎬 Video → Khmer Subtitles 🇰🇭")
st.write("Upload a video. Wait. Download Khmer subtitles.")

uploaded_video = st.file_uploader(
    "Drop video here",
    type=["mp4", "mkv", "avi", "mov"]
)

if uploaded_video:
    with tempfile.TemporaryDirectory() as tmp:
        video_path = os.path.join(tmp, uploaded_video.name)
        audio_path = os.path.join(tmp, "audio.wav")
        srt_path = os.path.join(tmp, "khmer.srt")

        # Save uploaded video
        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())

        with st.spinner("🔊 Extracting audio..."):
            extract_audio(video_path, audio_path)

        with st.spinner("📝 Transcribing speech..."):
            segments = transcribe_audio(audio_path)

        with st.spinner("🌍 Translating to Khmer..."):
            generate_srt(segments, translate_to_khmer, srt_path)

        with open(srt_path, "r", encoding="utf-8") as f:
            st.download_button(
                label="⬇️ Download Khmer Subtitles (.srt)",
                data=f,
                file_name="khmer.srt",
                mime="text/plain"
            )

        st.success("✅ Translation complete!")
