# backend/test/proprecessing/preprocessing_6.py

import re 
import tiktoken
import unidecode
import spacy
# import nltk
# import torch

# from torch.nn.functional import cosine_similarity
from nltk.tokenize import sent_tokenize
# from nltk.corpus import stopwords
from typing import List
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
# from sentence_transformers import SentenceTransformer

nlp = spacy.load("en_core_web_sm")
# model = SentenceTransformer('all-MiniLM-L6-v2')

# nltk.download('stopwords')
# nltk.download('punkt')

# stop_words = set(stopwords.words('english'))

# link_words = {
#     "and", "also", "in addition", "additionally", "furthermore", # addition
#     "moreover", "as well", "besides", "too", "not only that"
#     "but", "however", "although", "even though", "though", "yet", # contrast
#     "nevertheless", "nonetheless", "on the other hand", "despite",
#     "in contrast", "still", "whereas", "while", "instead", "conversely"
#     "because", "since", "as", "due to", "therefore", "thus", # cause n effect
#     "hence", "consequently", "so", "for this reason", "as a result"
#     "similarly", "likewise", "just as", "in the same way", "equally" # comparison
#     "indeed", "in fact", "certainly", "undoubtedly", "above all", # emphasis
#     "clearly", "obviously", "of course", "surely"
#     "for example", "for instance", "such as", "including", "namely", # illustration
#     "to illustrate", "in particular", "especially"
#     "first", "second", "third", "then", "next", "after", "afterward", # time sequence
#     "before", "eventually", "finally", "meanwhile", "subsequently",
#     "at the same time", "now", "later", "soon", "until", "when", "while"
#     "in conclusion", "to summarize", "to sum up", "overall", "in brief", # summary
#     "in short", "on the whole", "in a nutshell", "ultimately"
#     "if", "unless", "provided that", "as long as", "even if", "in case" # condition
#     "so that", "in order that", "to", "so", "for the purpose of" # purpose
# }

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

# def remove_stop_link_words(text: str) -> str:
#     print(f"[REMOVE_STOP_WORDS] Starting stop word removal.")
#     words = text.split()
#     filtered_words = [word for word in words if word.lower() not in stop_words and word.lower() not in link_words]
#     cleaned_text = ' '.join(filtered_words)
#     print(f"[REMOVE_STOP_WORDS] Stop word removal complete.")
#     return cleaned_text

# def clean_duplicate_sentences(text: str, threshold: float = 0.7) -> str:
#     sentences = sent_tokenize(text)
#     if len(sentences) <= 1:
#         return text
#     embeddings = model.encode(sentences, convert_to_tensor=True)
#     to_remove = set()
#     for i in range(len(sentences)):
#         if i in to_remove:
#             continue
#         for j in range(i + 1, len(sentences)):
#             sim = cosine_similarity(embeddings[i], embeddings[j], dim=0)
#             if sim > threshold:
#                 to_remove.add(j)
#     cleaned = [s for i, s in enumerate(sentences) if i not in to_remove]
#     return ' '.join(cleaned)

def compress_text_ner(text: str) -> str:
    sentences = sent_tokenize(text)
    informative_sentences = []

    for sentence in sentences:
        doc = nlp(sentence)
        if any(ent.label_ for ent in doc.ents):  # if there's at least one named entity
            informative_sentences.append(sentence)

    return " ".join(informative_sentences)

def compress_text_sumy(text: str, sentence_count: int = 5) -> str:

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def compress_text_sumy_dynamic(text: str) -> str:
    word_count = len(text.split())
    if word_count > 1000:
        return compress_text_sumy(text, sentence_count=8)
    elif word_count > 500:
        return compress_text_sumy(text, sentence_count=5)
    else:
        return text
    
def cleaning_ner_then_sumy(text: str, min_words: int = 100) -> str:
    ner_filtered = compress_text_with_ner(text)
    
    # If too short after NER, return original
    if len(ner_filtered.split()) < min_words:
        return text

    return compress_text_sumy_dynamic(ner_filtered)


def preprocessing_pipeline(text: str) -> List[str]:
    print(f"[PREPROCESSING_PIPELINE] Starting preprocessing pipeline.")
    text = remove_gutenberg_boilerplate(text)
    text = basic_clean(text)
    # text = remove_stop_link_words(text)
    # text = clean_duplicate_sentences(text)
    text = remove_toc_using_chapter_density(text)
    chunks = split_into_chapters(text)
    # chunks = [compress_text_ner(chunk) for chunk in chunks]
    chunks = [compress_text_sumy_dynamic(chunk) for chunk in chunks]
    print(f"[PREPROCESSING_PIPELINE] Preprocessing pipeline complete.")
    return chunks