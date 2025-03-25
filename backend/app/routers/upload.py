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


# def split_into_chapters(text: str, fallback_chunk_size: int = 1000) -> List[str]:
#     # Content table detection


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    logger.info(f"[upload_file] Received file upload: {file.filename}")

    try:
        content = await file.read()
        text = content.decode("utf-8", errors="replace")

        cleaned_text = remove_gutenberg_boilerplate(text)
        cleaned_text = basic_clean(cleaned_text)
        # chapters, chapter_texts = split_into_chapters(cleaned_text)

        logger.info(f"[upload_file] File '{file.filename}' processed successfully.")


        return {
            "filename": file.filename,
            "full_text": cleaned_text,
            # "num_chapters": len(chapters),
            # "chapters": [
            #     {
            #         "title": chapters[i],
            #         "text": chapter_texts[i],
            #     }
            #     for i in range(len(chapters))
            # ]
        }

    except ValueError as ve:
        logger.error(f"[upload_file] ValueError: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception(f"[upload_file] Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
