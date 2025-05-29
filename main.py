from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel
import uvicorn
import uuid
import os
import traceback
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
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://watchai-ten.vercel.app"],  # Change to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GCS_BUCKET_NAME ="watchai-bucket"

@app.get("/")
async def root():
    return {"message": "Hello from Render", "port": os.getenv("PORT")}

class VideoURLRequest(BaseModel):
    videoUrl: str




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
        print("Extracted Metadata")

        # Thumbnail
        thumbnail_path = extract_thumbnail(local_video_path)
        thumbnail_s3_key = f"thumbnails/{video_id}.jpg"
        upload_to_s3(thumbnail_path, thumbnail_s3_key)
        thumbnail_url = generate_s3_url(thumbnail_s3_key)
        print("Generated Thumbnail URL")

        # Transcript
        transcript, audio_path = transcribe_audio(local_video_path)
        print("Generated Transcript")

        # Summary
        summary = summarize_text(transcript)
        description = summary

        # Title
        title = generate_title(transcript)
        print("Title Made")

        # Subcategory
        subcategory = predict_subcategory(transcript, summary, title)

        # Audio Upload
        audio_s3_key = f"audio/{video_id}.wav"
        upload_to_s3(audio_path, audio_s3_key)
        audio_url = generate_s3_url(audio_s3_key)
        print("Audio Done")

        # Embeddings
        visual_emb = extract_visual_embedding(thumbnail_path)
        audio_emb = extract_audio_embedding(audio_path)
        text_emb = extract_text_embedding(transcript)
        combined_emb = combine_embeddings(visual_emb, audio_emb, text_emb)
        print("Embeddings Created")


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

        doc_id = store_video_metadata(payload,video_id)
        print(f"[✓] Stored video metadata in Firestore with ID: {doc_id}")

        #Faiss Index
        update_similar_videos()
        
        return {"videoId": doc_id, "metadata": payload}

    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()  # This prints the full traceback to your console/logs
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(local_video_path): os.remove(local_video_path)
        if os.path.exists(thumbnail_path): os.remove(thumbnail_path)
        if os.path.exists(audio_path): os.remove(audio_path)

@app.get("/process-video")
async def process_video_get(videoUrl: str = Query(..., alias="videoUrl")):
    return await process_video_api(VideoURLRequest(videoUrl=videoUrl))


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 7000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

