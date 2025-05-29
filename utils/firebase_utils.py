import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import numpy as np
import os
import json

def load_firebase_credentials():
    # This works both locally and on Cloud Run
    secret_path = "/secrets/firebase-creds"
    if os.path.exists(secret_path):
        with open(secret_path, "r") as f:
            return json.load(f)
    else:
        # fallback: load from local file for local testing
        fallback_path = os.path.join(os.path.dirname(__file__), '..', 'firebase-credentials.json')
        return json.load(open(fallback_path))

# Initialize Firebase only once
if not firebase_admin._apps:
    creds_dict = load_firebase_credentials()
    cred = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def store_video_metadata(data):
    doc_id = uuid.uuid4().hex
    db.collection("videos").document(doc_id).set(data)
    return doc_id

def get_all_video_embeddings():
    video_docs = db.collection("videos").stream()
    embeddings = []

    for doc in video_docs:
        data = doc.to_dict()
        emb = data.get("embeddings", {}).get("combined")
        if emb and isinstance(emb, list) and len(emb) > 0:
            embeddings.append((doc.id, np.array(emb, dtype=np.float32)))

    return embeddings
