import os
from dotenv import load_dotenv
from importlib import import_module

# prefer .env.local
if os.path.exists('.env.local'):
    load_dotenv('.env.local')
else:
    load_dotenv()

PROVIDER = os.getenv('LLM_PROVIDER', 'fake')

if PROVIDER == 'openai':
    module = import_module('app.core.llm.openai')
else:
    module = import_module('app.core.llm.fake')


async def generate(prompt: str, max_tokens: int = 250):
    return await module.generate(prompt, max_tokens=max_tokens)
