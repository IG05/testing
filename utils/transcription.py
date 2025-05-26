import os
import subprocess
import tempfile
from transformers import pipeline
import shutil
import uuid

# Load Whisper ASR model (English-only small)
asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small.en",
    return_timestamps=True
)

def extract_audio_from_video(video_path, audio_path):
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        audio_path,
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

def transcribe_audio(video_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_audio_path = os.path.join(tmpdir, "temp_audio.wav")
        extract_audio_from_video(video_path, tmp_audio_path)

        if not os.path.exists(tmp_audio_path):
            raise FileNotFoundError(f"Failed to create audio file at {tmp_audio_path}")

        # Copy to a permanent temp location before the tempdir is deleted
        final_audio_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.wav")
        shutil.copy(tmp_audio_path, final_audio_path)

    # Now outside the context — `final_audio_path` is safe
    result = asr(final_audio_path)

    return result["text"],final_audio_path
