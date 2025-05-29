import numpy as np
import faiss
from firebase_admin import firestore
from tqdm import tqdm

TOP_K = 3  # Number of similar videos to cache per video
db = firestore.client()


def update_similar_videos():
    """
    Rebuilds FAISS index and updates top-K similar videos for each video in Firestore.
    """
    print("[+] Fetching all video embeddings from Firestore...")
    video_docs = list(db.collection("videos").stream())
    embeddings = []
    video_ids = []

    for doc in tqdm(video_docs):
        data = doc.to_dict()
        emb = data.get("combinedEmbedding")
        if isinstance(emb, list) and emb:
            embeddings.append(np.array(emb, dtype=np.float32))
            video_ids.append(doc.id)

    if not embeddings:
        print("❌ No embeddings found in Firestore!")
        return

    embedding_matrix = np.vstack(embeddings)
    dim = embedding_matrix.shape[1]
    print(f"[✓] Loaded {len(embeddings)} embeddings with dimension {dim}")

    # Build FAISS index
    print("[+] Building FAISS index...")
    faiss.normalize_L2(embedding_matrix)
    index = faiss.IndexFlatIP(dim)
    index.add(embedding_matrix)

    # Search similar videos
    print(f"[+] Searching top-{TOP_K} similar videos for each video...")
    distances, indices = index.search(embedding_matrix, TOP_K + 1)

    for i, video_id in enumerate(video_ids):
        similar = []
        for j, idx in enumerate(indices[i]):
            if idx == i or idx >= len(video_ids):
                continue

            score = float(distances[i][j])
            if score < -1e5:
                continue

            similar.append({
                "videoId": video_ids[idx],
                "score": round(score, 6)
            })

            if len(similar) >= TOP_K:
                break

        db.collection("recommendations").document(video_id).set({
            "videoId": video_id,
            "similar": similar
        })

    print("✅ Recommendations updated for all videos in Firestore.")
