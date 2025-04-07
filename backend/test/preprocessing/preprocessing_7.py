import time 

from backend.test.preprocessing.preprocessing_6 import preprocessing_pipeline

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def compress_text_sumy(text: str, sentence_count: int = 5) -> str:

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def compress_dynamic(text: str) -> str:
    word_count = len(text.split())
    if word_count > 1000:
        return compress_text_sumy(text, sentence_count=8)
    elif word_count > 500:
        return compress_text_sumy(text, sentence_count=5)
    else:
        return text
    
if __name__ == "__main__":
    with open("backend/test/data/echoes.txt", 'r') as f:
        dummy_text = f.read()
    start_total = time.time()
    chunks = preprocessing_pipeline(dummy_text)
    