import urllib.request
import json
from . import storage
from .toolbox import console, warning

def get_ai_feedback(prompt: str) -> str:
    config = storage.load_data(storage.AI_CONFIG)
    if not config or not isinstance(config, dict):
        return "AI Accountability not configured. Please set your API keys in Settings."

    provider = config.get("provider")
    api_key = config.get("api_key")

    if not api_key:
        return "API key missing. Please check your AI Accountability settings."

    system_prompt = (
        "You are David Goggins. Your job is to provide accountability and motivation. "
        "Be raw, be real, and be blunt. If the user is making excuses, call them out. "
        "Your goal is to help them callous their mind and achieve their goals. STAY HARD!"
    )

    try:
        if provider == "OpenAI" or provider == "OpenRouter":
            url = "https://api.openai.com/v1/chat/completions"
            model = "gpt-4o"
            if provider == "OpenRouter":
                url = "https://openrouter.ai/api/v1/chat/completions"
                model = "meta-llama/llama-3.1-405b-instruct"

            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode())
                return res_data["choices"][0]["message"]["content"]

        elif provider == "Anthropic":
            url = "https://api.anthropic.com/v1/messages"
            data = {
                "model": "claude-3-5-sonnet-20240620",
                "max_tokens": 1024,
                "system": system_prompt,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }

            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode())
                return res_data["content"][0]["text"]

        else:
            return "Unknown AI provider selected."

    except Exception as e:
        return f"AI Error: {str(e)}"
