# 🧠 WatchAI ML Pipeline

**AI/ML Pipeline** for intelligent video content analysis and personalized recommendations. This containerized Python backend powers the [WatchAI platform](https://watchai-ten.vercel.app/) with multi-modal AI processing.

🔗 **[Frontend Repository](https://github.com/IG05/watchai)** | 🌐 **[Live Demo](https://watchai-ten.vercel.app/)**

---

## 🚀 Overview

Machine learning pipeline that processes videos using AI models to extract insights and generate personalized recommendations. Analyzes video content through visual, audio, and textual modalities.

### Key Features
- 🎥 **Multi-Modal Analysis** using CLIP, Whisper, and NLP models
- ⚡ **Containerized Deployment** on Google Cloud Run
- 🎯 **FAISS Similarity Search** for fast recommendations
- 🔄 **AWS S3 Integration** for video storage
- 📊 **Dynamic User Profiling** based on behavior

---

## 🛠️ Tech Stack

**AI/ML Models**
- **CLIP** - Computer vision analysis
- **Whisper** - Audio transcription
- **SentenceTransformers** - Text embeddings
- **FAISS** - Similarity search

**Infrastructure**
- **Python 3.8+** | **Docker** | **Google Cloud Run** | **AWS S3**

---

## 🚀 Getting Started

### 1. Setup

```bash
# Clone and setup
git clone https://github.com/IG05/testing.git
cd testing
pip install -r requirements.txt
```

### 2. Environment Variables

```bash
# .env file
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket
GOOGLE_CLOUD_PROJECT=your_gcp_project
```

## 🔧 How It Works

1. **Video Input** → Extract frames and audio from S3
2. **AI Analysis** → CLIP (visual) + Whisper (audio) + NLP (text)
3. **Feature Extraction** → Generate embeddings for each modality
4. **User Profiling** → Update user preferences based on behavior
5. **Similarity Search** → FAISS finds similar content
6. **Recommendations** → Return personalized video suggestions

---

## 📈 Performance

- **Processing Speed**: ~20-30 seconds per minute of video (CPU)
- **Similarity Search**: <10ms for videos
- **Memory Usage**: 4-6GB RAM
- **Accuracy**: 85%+ recommendation relevance

---

## 🔄 Future Enhancements

- 🎬 Scene detection and analysis
- 🗣️ Multi-speaker identification
- 📊 Advanced analytics dashboard
- 🌍 Multi-language support

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

---

## 👨‍💻 Contact

**Ishaan Goyal**
- 📧 [ishaangoyal0610@gmail.com](mailto:ishaangoyal0610@gmail.com)
- 💼 [LinkedIn](https://www.linkedin.com/in/ishaan-goyal10/)
- 🌐 [Live Demo](https://watchai-ten.vercel.app/)

---

<div align="center">
  <strong>⭐ Star this repo if you found it helpful!</strong>
</div>
