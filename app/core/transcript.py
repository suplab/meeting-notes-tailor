from typing import List, Dict
import re


def parse_transcript(text: str) -> List[Dict]:
    segments = []
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    timestamp_re = re.compile(r"\\[(\\d{1,2}:\\d{2}:\\d{2})\\]")
    for line in lines:
        ts = None
        m = timestamp_re.match(line)
        if m:
            ts = m.group(1)
            line = line[m.end():].strip()
        if ':' in line:
            speaker, rest = line.split(':', 1)
            segments.append({'speaker': speaker.strip(), 'start': ts, 'text': rest.strip()})
        else:
            if segments:
                segments[-1]['text'] += ' ' + line
            else:
                segments.append({'speaker': 'unknown', 'start': ts, 'text': line})
    return segments


def chunk_segments(segments, max_chars=1500):
    chunks = []
    cur = []
    cur_len = 0
    for s in segments:
        piece = f"[{s.get('start') or ''}] {s['speaker']}: {s['text']}\\n"
        if cur_len + len(piece) > max_chars and cur:
            chunks.append("\\n".join(cur))
            cur = [piece]
            cur_len = len(piece)
        else:
            cur.append(piece)
            cur_len += len(piece)
    if cur:
        chunks.append("\\n".join(cur))
    return chunks
