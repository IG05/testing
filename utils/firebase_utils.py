import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import numpy as np
import os

# Automatically uses service account file in root directory
FIREBASE_CRED_PATH = os.path.join(os.path.dirname(__file__), '..', 'firebase-credentials.json')

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def store_video_metadata(data):
    doc_id = uuid.uuid4().hex
    db.collection("videos").document(doc_id).set(data)
    return doc_id


def get_all_video_embeddings():
    """
    Returns list of (videoId, combined_embedding np.ndarray)
    """
    video_docs = db.collection("videos").stream()
    embeddings = []

    for doc in video_docs:
        data = doc.to_dict()
        emb = data.get("embeddings", {}).get("combined")
        if emb and isinstance(emb, list) and len(emb) > 0:
            embeddings.append((doc.id, np.array(emb, dtype=np.float32)))

    return embeddings