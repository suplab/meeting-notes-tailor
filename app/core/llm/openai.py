import os
import asyncio
import openai


async def generate(prompt: str, max_tokens: int = 250) -> str:
    # OpenAI python library is sync; run in thread to avoid blocking uvicorn
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('MODEL_NAME', 'gpt-4o-mini')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY not set for OpenAI provider')
    openai.api_key = api_key

    def _call():
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.2,
        )
        return resp['choices'][0]['message']['content']

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _call)
