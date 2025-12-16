import os
import requests
from openai import OpenAI
from core.vars import OLLAMA_URL, MODEL
from google import genai
from google.genai import types

def text_to_sql(text: str) -> str:
    ASSETS_ROOT = os.getenv("ASSETS_ROOT")
    AI_API_KEY = os.getenv("AI_API_KEY")
    AI_PROVIDER = os.getenv("AI_PROVIDER")
    DEBUG = os.getenv("DEBUG") == "True"
    prompt = ""

    with open(os.path.join(ASSETS_ROOT, "prompt_new.txt"), "r", encoding="utf-8") as f:
        prompt = f.read()
        print("PROMPT:")
        print(prompt)

    if not DEBUG:
        if AI_PROVIDER == "google":
            client = genai.Client(api_key=AI_API_KEY)

            response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=prompt,
                    temperature = 0,
                    top_p = 0.99,
                    top_k = 0,
                    max_output_tokens = 4096
                ),
            )

            result = response.text.strip()
        else:
            client = OpenAI(api_key=AI_API_KEY, base_url="https://api.deepseek.com")
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                stream=False,
                temperature=0
            )
            result = resp.choices[0].message.content.strip()
    else:
        print(MODEL)
        print(text)
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "system": prompt,
                "prompt": text,
                # "think": True,
                "stream": False,
                "options": {
                    "temperature": 0
                }
            },
            timeout=120
        )

        response.raise_for_status()
        data = response.json()

        result = data["response"].strip()

    start_i = 0
    end_i = len(result) - 1

    print(result)

    while not result[start_i:].lower().startswith("select") and start_i < len(result):
        start_i += 1
    while not result[:end_i+1].lower().endswith(";") and end_i > 0:
        end_i -= 1

    # Ollama возвращает текст в поле response
    return result[start_i:end_i+1]
    
