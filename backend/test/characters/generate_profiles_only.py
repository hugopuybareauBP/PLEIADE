import json
import re
from collections import defaultdict
from ollama import chat
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

# Initialize console
console = Console()

def extract_character_notes(raw_summary: str):
     character_notes = {}

     for line in raw_summary.splitlines():
          line = line.strip()
          if line.startswith("- Characters:"):
               characters_line = line.split(":", 1)[1]
               characters = [c.strip() for c in characters_line.split(",") if c]
          elif line.startswith("- Character Notes:"):
               continue
          elif line.startswith("- Events:"):
               break
          elif line.startswith("- ") or line.startswith("• "):
               match = re.match(r"[-•]\s*(\w+):\s*(.*)", line)
               if match:
                    char_name, note = match.groups()
                    character_notes[char_name] = note
     return character_notes

def aggregate_character_notes(summaries, top_c: int = 5):
     aggregated_notes = defaultdict(list)
     mention_counts = defaultdict(int)

     for summary in summaries:
          character_notes = extract_character_notes(summary["raw_output"])
          for char, note in character_notes.items():
               aggregated_notes[char].append(note)
               mention_counts[char] += 1    
     
     most_frequent_characters = sorted(mention_counts.items(), key=lambda x: x[1], reverse=True)[:top_c]
     console.print("\n[bold blue]🏆 Top characters (by mentions):[/]")
     for char, count in most_frequent_characters:
          console.print(f"• {char} ({count} mentions)")

     top_character_names = {char for char, _ in most_frequent_characters}
     filtered_notes = {char: aggregated_notes[char] for char in top_character_names}
     return filtered_notes

def generate_final_profiles(character_memory):
     profiles = {}

     with Progress() as progress:
          task = progress.add_task("[cyan]Summarizing...", total=len(character_memory))
          for character, notes in character_memory.items():
               prompt = (
                    f"Based on the following notes about the character {character}, "
                    f"write a complete character profile including:\n"
                    f"- Personality traits\n- Role in the story\n- Key events and relationships\n\n"
                    f"Notes:\n{chr(10).join(['- ' + n for n in notes])}"
               )

               response = chat(
                    model="mistral",
                    messages=[{"role": "user", "content": prompt}]
               )

               profiles[character] = response["message"]["content"]
               progress.update(task, advance=1)

     return profiles

if __name__ == "__main__":

     filepath = "./summaries/alice_summaries_for_profile.json"  
     with open(filepath, "r", encoding="utf-8") as f:
          summaries = json.load(f)

     console.print(Panel("[bold cyan]🧠 Loading summaries and extracting character notes..."))
     character_memory = aggregate_character_notes(summaries, top_c=5)

     console.print(Panel("[bold magenta]📖 Generating final character profiles..."))
     final_profiles = generate_final_profiles(character_memory)
     for character, profile in final_profiles.items():
          console.print(Panel(f"[bold blue]=== {character.upper()} ===", expand=False))
          console.print(profile)

     