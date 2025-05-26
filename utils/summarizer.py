from openai import OpenAI

from dotenv import load_dotenv
import os


load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)

def summarize_text(text):
    prompt = f"Summarize the following video transcript into a short, informative paragraph (2-3 sentences):\n\n{text}\n\nSummary:"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at summarizing news video transcripts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.5
    )
    
    summary = response.choices[0].message.content.strip()
    return summary
