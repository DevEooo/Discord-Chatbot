def split_into_chunks(text: str, size: int = 1900) -> list[str]: # From long text string convert into 1900 int chunks and put into list 
    if not text:
        return [""]
    return [text[i:i + size] for i in range(0, len(text), size)]