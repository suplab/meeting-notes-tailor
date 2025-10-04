TEMPLATES = {
    'exec': (
        'You are a concise executive assistant. Given the transcript excerpt, produce a 3-sentence summary '
        'emphasizing strategic decisions, risks, and senior-level requests. Return only the summary text.\\n\\nTranscript:\\n{chunk}'
    ),
    'actions': (
        'You are a product ops assistant. From the transcript excerpt, extract concrete action items. '
        'For each action return a single line formatted as: TASK | OWNER(if any) | DUE(if any) | CONTEXT. Return one action per line.\\n\\nTranscript:\\n{chunk}'
    ),
    'recap': (
        'You are explaining to a new joiner. Provide a short plain-language recap (4-6 sentences) of what happened and why it matters. Return only the text.\\n\\nTranscript:\\n{chunk}'
    ),
}
