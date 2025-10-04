from typing import Dict, Any
from app.core.transcript import parse_transcript, chunk_segments
from app.core.prompt_templates import TEMPLATES
from app.core.llm import generate
import asyncio


async def _summarize_chunk(chunk: str, role: str) -> str:
    prompt = TEMPLATES[role].format(chunk=chunk)
    return await generate(prompt)


async def generate_multilayer_summary(transcript_text: str, include_sentiment: bool = False) -> Dict[str, Any]:
    segments = parse_transcript(transcript_text)
    chunks = chunk_segments(segments)

    roles = {'exec': [], 'actions': [], 'recap': []}

    tasks = []
    for chunk in chunks:
        tasks.append(_summarize_chunk(chunk, 'exec'))
        tasks.append(_summarize_chunk(chunk, 'actions'))
        tasks.append(_summarize_chunk(chunk, 'recap'))

    results = await asyncio.gather(*tasks)

    for i in range(0, len(results), 3):
        roles['exec'].append(results[i].strip())
        roles['actions'].append(results[i + 1].strip())
        roles['recap'].append(results[i + 2].strip())

    executive_summary = '\\n\\n'.join(roles['exec'])[:1200]
    team_actions_raw = '\\n'.join(roles['actions']).splitlines()
    seen = set()
    team_actions = []
    for a in team_actions_raw:
        s = a.strip()
        if not s:
            continue
        if s in seen:
            continue
        seen.add(s)
        parts = [p.strip() for p in s.split('|')]
        while len(parts) < 4:
            parts.append('')
        team_actions.append({'task': parts[0], 'owner': parts[1], 'due': parts[2], 'context': parts[3]})

    plain_recap = '\\n\\n'.join(roles['recap'])[:2000]

    out = {
        'executive_summary': executive_summary,
        'team_actions': team_actions,
        'plain_recap': plain_recap,
    }

    if include_sentiment:
        speakers = {s['speaker'] for s in segments}
        out['sentiment'] = {sp: 'neutral' for sp in speakers}

    return out
