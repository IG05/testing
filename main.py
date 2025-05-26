from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import uuid
import os
from utils.ffmpeg_utils import extract_metadata, extract_thumbnail, download_video
from utils.transcription import transcribe_audio
from utils.summarizer import summarize_text
from utils.embeddings import (
    extract_visual_embedding, extract_audio_embedding,
    extract_text_embedding, combine_embeddings
)
from utils.firebase_utils import store_video_metadata
from utils.categorization import predict_subcategory
from utils.title_generator import generate_title
from utils.s3_utils import upload_to_s3, generate_s3_url
from datetime import datetime
from utils.similar_videos import update_similar_videos


app = FastAPI()

class VideoURLRequest(BaseModel):
    videoUrl: str

@app.get("/")
async def root():
    return {"message": "API is running. Use POST /process-video to process videos."}


@app.post("/process-video")
async def process_video_api(req: VideoURLRequest):
    video_url = req.videoUrl
    video_id = str(uuid.uuid4())
    local_video_path = f"{video_id}.mp4"

    try:
        print("[+] Downloading video...")
        download_video(video_url, local_video_path)

        # Metadata
        meta = extract_metadata(local_video_path)

        # Thumbnail
        thumbnail_path = extract_thumbnail(local_video_path)
        thumbnail_s3_key = f"thumbnails/{video_id}.jpg"
        upload_to_s3(thumbnail_path, thumbnail_s3_key)
        thumbnail_url = generate_s3_url(thumbnail_s3_key)

        # Transcript
        transcript, audio_path = transcribe_audio(local_video_path)

        # Summary
        summary = summarize_text(transcript)
        description = summary

        # Title
        title = generate_title(transcript)

        # Subcategory
        subcategory = predict_subcategory(transcript, summary, title)

        # Audio Upload
        audio_s3_key = f"audio/{video_id}.wav"
        upload_to_s3(audio_path, audio_s3_key)
        audio_url = generate_s3_url(audio_s3_key)

        # Embeddings
        visual_emb = extract_visual_embedding(thumbnail_path)
        audio_emb = extract_audio_embedding(local_video_path)
        text_emb = extract_text_embedding(transcript)
        combined_emb = combine_embeddings(visual_emb, audio_emb, text_emb)


        # Upload metadata
        payload = {
            "videoId": video_id,
            "videoUrl": video_url,
            "title": title,
            "transcript": transcript,
            "description": summary,
            "subCategory": subcategory,
            "publishedAt": datetime.now().isoformat(),
            "duration": meta["duration"],
            "tags": [],
            "category": "news",
            "thumbnailUrl": thumbnail_url,
            "visualFeatures": visual_emb,
            "audioFeatures": audio_emb,
            "textEmbedding": text_emb,
            "combinedEmbedding": combined_emb
        }

        doc_id = store_video_metadata(payload)
        print(f"[✓] Stored video metadata in Firestore with ID: {doc_id}")

        #Faiss Index
        update_similar_videos()
        
        return {"status": "success", "videoId": doc_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(local_video_path): os.remove(local_video_path)
        if os.path.exists(thumbnail_path): os.remove(thumbnail_path)
        if os.path.exists(audio_path): os.remove(audio_path)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
