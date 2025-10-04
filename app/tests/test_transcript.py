from app.core.transcript import parse_transcript


def test_basic_parse():
    text = "[00:00:01] Alice: Hello\nBob: hi"
    segs = parse_transcript(text)
    assert len(segs) == 2
    assert segs[0]['speaker'] == 'Alice'
    assert segs[1]['speaker'] == 'Bob'
