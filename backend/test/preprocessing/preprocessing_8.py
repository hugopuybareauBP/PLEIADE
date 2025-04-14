# backend/test/proprecessing/preprocessing_6.py

import re 
import tiktoken
import unidecode

from typing import List
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

enc = tiktoken.get_encoding("cl100k_base")

def remove_gutenberg_boilerplate(text: str) -> str:
    print("[REMOVE_GUTENBERG_BOILERPLATE] Attempting to remove Gutenberg boilerplate.")

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    # Find start
    start_index = text.find(start_marker)
    if start_index != -1:
        start_index = text.find("\n", start_index)
        if start_index != -1:
            text = text[start_index:].strip()
        else:
            print(f"[REMOVE_GUNTENBERG_BOILERPLATE] Newline after start marker not found. Returning full text.")
    else:
        print(f"[REMOVE_GUTENBERG_BOILERPLATE] Start marker not found. Returning full text.")

    # Find end
    end_index = text.find(end_marker)
    if end_index != -1:
        text = text[:end_index].strip()
    else:
        print(f"[REMOVE_GUTENBERG_BOILERPLATE] End marker not found. Returning full text.")

    print("[REMOVE_GUTENBERG_BOILERPLATE] Processing complete.")
    return text

def basic_clean(text: str) -> str:

        print(f"[BASIC_CLEAN] Starting basic cleaning of text.")

        # Convert non-ASCII characters (accents, special chars) to closest ASCII equivalents
        text = unidecode.unidecode(text)

        text = text.replace("\r\n", "\n")
        text = re.sub(r"\n\s*\n", "\n\n", text)
        text = text.strip()

        print(f"[BASIC_CLEAN] Basic cleaning complete.")
        return text

def get_token_count(text: str) -> int:
    return len(enc.encode(text))

def remove_toc_using_chapter_density(text: str, max_gap_tokens: int = 100) -> str:
    chapter_pattern = re.compile(r'(chapter\s+\d+|chapter\s+[ivxlc]+)', re.IGNORECASE)
    matches = list(chapter_pattern.finditer(text))

    print(f"[REMOVE_TOC_USING_CHAPTER_DENSITY] Found {len(matches)} candidates.")

    for i in range(len(matches) - 1):
        current = matches[i]
        next_one = matches[i + 1]
        in_between = text[current.end():next_one.start()]
        gap_tokens = get_token_count(in_between)

        # still in the toc
        if gap_tokens <= max_gap_tokens:
            continue
        else:
            # first real chapter
            print(f"[REMOVE_TOC_USING_CHAPTER_DENSITY] First real chapter at position {current.start()}, gap to next: {gap_tokens} tokens")
            return text[current.start():]

    print("[REMOVE_TOC_USING_CHAPTER_DENSITY] Could not determine TOC end — returning original text.")
    return text

def split_into_chapters(text: str, fallback_chunk_size: int = 1000) -> List[str]:
    text = remove_toc_using_chapter_density(text) # TOC removal

    chapter_pattern = re.compile(r'(chapter\s+(?:\d+|[ivxlc]+))\b', re.IGNORECASE) # regex for chapter headings
    chapter_matches = list(chapter_pattern.finditer(text))

    if len(chapter_matches) >= 2:
        print(f"[SPLIT_INTO_CHAPTERS] {len(chapter_matches)} chapter headings detected.")
        chunks = []
        for i in range(len(chapter_matches)):
            start = chapter_matches[i].start()
            end = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(text)
            chunks.append(text[start:end].strip())
        return chunks

    print("[SPLIT_INTO_CHAPTERS] No structure found — fallback to chunking.") 
    words = text.split()
    chunks = []
    for i in range(0, len(words), fallback_chunk_size):
        chunk = ' '.join(words[i:i+fallback_chunk_size])
        chunks.append(chunk)
    return chunks

def compress_text_sumy(text: str, sentence_count: int = 5) -> str:

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def compress_chapter_safe(text: str, min_words: int = 100, threshold_words: int = 500) -> str:

    word_count = len(text.split())
    
    if word_count < threshold_words:
        return text

    compressed = compress_text_sumy(text, sentence_count=30 if word_count > 1000 else 25)
    if len(compressed.split()) < min_words:
        return text  # revert if too agressive

    return compressed


def preprocessing_pipeline(text: str) -> List[str]:
    print(f"[PREPROCESSING_PIPELINE] Starting preprocessing pipeline.")
    text = remove_gutenberg_boilerplate(text)
    text = basic_clean(text)
    text = remove_toc_using_chapter_density(text)
    chunks = split_into_chapters(text)
    chunks = [compress_chapter_safe(chunk) for chunk in chunks]
    print(f"[PREPROCESSING_PIPELINE] Preprocessing pipeline complete.")
    return chunks