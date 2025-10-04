import asyncio


async def generate(prompt: str, max_tokens: int = 250) -> str:
    p = prompt.lower()
    if 'executive' in p:
        return 'Strategic decision: adopt API-first approach. Risk: timeline tight. Ask: leadership to approve extra headcount.'
    if 'product ops' in p or 'action' in p:
        return 'Define API contract | Alice | 2025-10-20 | Discussed API shape;\\nPrepare migration plan | Bob | 2025-11-01 | Requires infra sign-off'
    if 'new joiner' in p or 'explain' in p:
        return 'This meeting described the plan to migrate to an API-first architecture, the next steps, and who owns what. Key milestones were discussed and a couple of deadlines were proposed.'
    await asyncio.sleep(0.01)
    return '(fake llm response)'
