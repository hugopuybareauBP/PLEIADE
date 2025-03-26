    # backend/app/routers/upload.py

import re
import logging

from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
from unidecode import unidecode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def remove_gutenberg_boilerplate(text: str) -> str:
        """
        Function to remove Gutenberg header/footer from text.
        """
        logger.info("[remove_gutenberg_boilerplate] Removing header/footer from text.")

        start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
        end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

        # Find the start marker
        start_index = text.find(start_marker)
        if start_index == -1:
            logger.error("Start marker not found.")
            raise ValueError("Start marker not found in text")
        start_index = text.find("\n", start_index)
        if start_index == -1:
            logger.error("Newline after start marker not found.")
            raise ValueError("Newline after start marker not found in text")
        text = text[start_index:].strip()

        # Find the end marker
        end_index = text.find(end_marker)
        if end_index == -1:
            logger.error("End marker not found.")
            raise ValueError("End marker not found in text")
        text = text[:end_index].strip()

        logger.info("[remove_gutenberg_boilerplate] Boilerplate removed successfully.")
        return text


def basic_clean(text: str) -> str:

        logger.info("[basic_clean] Starting basic cleaning of text.")

        # Convert non-ASCII characters (accents, special chars) to closest ASCII equivalents
        text = unidecode(text)

        text = text.replace("\r\n", "\n")
        text = re.sub(r"\n\s*\n", "\n\n", text)
        text = text.strip()

        logger.info("[basic_clean] Basic cleaning complete.")
        return text


def split_into_chapters(text: str, fallback_chunk_size: int = 1000) -> List[str]:

    # Content table detection 
    ct_pattern = re.compile(r"(table of contents|contents|toc)([\s\S]{0,10000})", re.IGNORECASE) # if i dont put the a limit, it will grab full book
    ct_match = re.search(ct_pattern, text)
        
    if ct_match: # found one
        print(f"CT detected")
        ct_block = ct_match.group(2)
        chapter_lines = re.findall(r'(chapter\s+(?:\d+|[ivxlc]+).*?)\n', ct_block, re.IGNORECASE)

        if chapter_lines:
            last_heading = chapter_lines[-1]
            heading_pattern = re.escape(last_heading.strip())
            last_heading_match = list(re.finditer(heading_pattern, text, re.IGNORECASE))

            if last_heading_match:
                ct_end = last_heading_match[0].end()
                print(f"Removed {text[:ct_end]}")
                text = text[ct_end:]
                    
    # Look for chapter in the text
    chapter_pattern = r'(chapter\s+(?:\d+|[ivxlc]+))\b' # strict so it doesnt match 'in this chapter ...' 
    chapter_matches = list(re.finditer(chapter_pattern, text, re.IGNORECASE))

    if len(chapter_matches) >= 2:
        print(f"{len(chapter_matches)} chapters detected via headings.")
        chunks = []
        for i in range(len(chapter_matches)):
            start = chapter_matches[i].start()
            end = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(text)
            chunks.append(text[start:end].strip())
        return chunks

        # split into fixed-length chunks
        print("No structure found — fallback to chunking.")
        words = text.split()
        chunks = []
        for i in range(0, len(words), fallback_chunk_size):
            chunk = ' '.join(words[i:i+fallback_chunk_size])
            chunks.append(chunk)
        return chunks


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

        logger.info(f"[upload_file] Received file upload: {file.filename}")

        try:
            content = await file.read()
            text = content.decode("utf-8", errors="replace")

            cleaned_text = remove_gutenberg_boilerplate(text)
            cleaned_text = basic_clean(cleaned_text)
            chunks = split_into_chapters(cleaned_text)

            logger.info(f"[upload_file] File '{file.filename}' processed successfully.")


            return {
                "filename": file.filename,
                "full_text": cleaned_text,
                "chunk": [
                    {
                        "chunk_id": i,
                        f"chunk_text": chunks[i]
                    }
                    for i in range(len(chunks))
                ]
            }

        except ValueError as ve:
            logger.error(f"[upload_file] ValueError: {str(ve)}")
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            logger.exception(f"[upload_file] Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
