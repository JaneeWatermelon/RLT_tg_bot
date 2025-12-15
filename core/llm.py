import os
import requests
from openai import OpenAI
from core.vars import OLLAMA_URL, MODEL

def text_to_sql(text: str) -> str:
    ASSETS_ROOT = os.getenv("ASSETS_ROOT")
    DEBUG = os.getenv("DEBUG") == "True"
    prompt = ""

    with open(os.path.join(ASSETS_ROOT, "prompt.txt"), "r", encoding="utf-8") as f:
        prompt = f.read()
        print("PROMPT:")
        print(prompt)

    if not DEBUG:
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        return resp.choices[0].message.content.strip()
    else:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "system": prompt,
                "prompt": text,
                "think": False,
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

        # print(result)

        while not result[start_i:].lower().startswith("select"):
            start_i += 1
        while not result[:end_i+1].lower().endswith(";"):
            end_i -= 1

        # Ollama возвращает текст в поле response
        return result[start_i:end_i+1]
    
