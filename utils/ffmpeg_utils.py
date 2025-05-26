import subprocess
import os
import uuid
from PIL import Image
import requests  # Add this import for downloading videos
import tempfile
import shutil

def download_video(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def extract_metadata(video_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,duration", "-of", "default=noprint_wrappers=1", video_path],
        capture_output=True,
        text=True
    )
    metadata = {}
    for line in result.stdout.strip().split("\n"):
        if '=' in line:
            key, value = line.strip().split('=')
            metadata[key] = value
    return {
        "width": int(metadata.get("width", 0)),
        "height": int(metadata.get("height", 0)),
        "duration": float(metadata.get("duration", 0))
    }

def extract_thumbnail(video_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        thumbnail_path = os.path.join(tmpdir, f"{uuid.uuid4().hex}.jpg")
        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-ss", "00:00:01.000", "-vframes", "1",
            thumbnail_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if not os.path.exists(thumbnail_path):
            raise FileNotFoundError(f"Failed to create thumbnail at {thumbnail_path}")

        final_temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.jpg")
        shutil.copy(thumbnail_path, final_temp_path)
        return final_temp_path

