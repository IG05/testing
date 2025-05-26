import os
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)

def generate_title(text):
    prompt = f"Generate a concise, catchy, and relevant title for the following text:\n\n{text}\n\nTitle:"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates video titles."},
            {"role": "user", "content": f"Generate a good video title for this transcript: {text}"}
        ],
        max_tokens=30,
        temperature=0.7,
    )
    
    # ✅ Extract and return only the title string
    title = response.choices[0].message.content.strip().strip('"')
    return title


