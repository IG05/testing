from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)

# Valid news subcategories
CATEGORIES = ["politics", "sports", "technology", "entertainment", "business", "health", "science", "general", "war"]

def predict_subcategory(transcript: str, summary: str, title: str) -> str:
    # Build the prompt
    prompt = f"""
You are an expert news video classifier.

Your job is to classify a video into one of the following categories:
{CATEGORIES}

Use the transcript, summary, and title to infer the most accurate category.

Transcript:
{transcript[:1500]}

Summary:
{summary[:500]}

Title:
{title}

Return only the category name.
"""

    # Send request to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that classifies news videos into subcategories."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0,
        max_tokens=10
    )

    # Parse and validate response
    category = response.choices[0].message.content.strip().lower()
    return category if category in CATEGORIES else "general"
