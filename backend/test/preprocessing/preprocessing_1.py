import re
from typing import List

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

def test(file_path):
	with open(file_path, 'r') as file:
		text = file.read()
		
	chunks = split_into_chapters(text)
	print(f"\n=== Result: {len(chunks)} chunks ===\n")
	for i, chunk in enumerate(chunks[1:2]):  # show first 3
		print(f"\n--- Chunk {i+1} ---\n")
		print(chunk)  # print first 1000 chars
		print("\n...\n")

test("backend/test/data/alice_in_wonderland.txt")