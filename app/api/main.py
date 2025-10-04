from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
import os
from app.schemas import SummarizeRequest
from app.core.summarizer import generate_multilayer_summary

# prefer .env.local, else .env
if os.path.exists('.env.local'):
    load_dotenv('.env.local')
else:
    load_dotenv()

app = FastAPI(title='meeting-notes-tailor')


@app.get('/healthz')
async def healthz():
    mode = os.getenv('LLM_PROVIDER', 'fake')
    return {'status': 'ok', 'mode': mode}


@app.post('/summarize')
async def summarize(req: SummarizeRequest):
    try:
        result = await generate_multilayer_summary(req.transcript, include_sentiment=req.options.include_sentiment)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
