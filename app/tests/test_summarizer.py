import asyncio
from app.core.summarizer import generate_multilayer_summary


def test_summarizer_fake():
    transcript = "Alice: we will adopt API-first. Bob: action: prepare plan"
    res = asyncio.get_event_loop().run_until_complete(generate_multilayer_summary(transcript))
    assert 'executive_summary' in res
    assert isinstance(res['team_actions'], list)
