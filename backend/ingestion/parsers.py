def parse_patent_text(text: str) -> dict:
    return {"title": text.splitlines()[0] if text else "Untitled", "content": text}
