from pathlib import Path
import json
from difflib import get_close_matches
from typing import Dict, List, Union, Optional
from dataclasses import dataclass

@dataclass
class DictionaryEntry:
  word: str
  meanings: Dict[str, List[str]]
  antonyms: List[str]
  synonyms: List[str]


class DictionaryLoader:
  def __init__(self, data_folder: str = "data/"):
    self.data_folder = Path(data_folder)

  def load_dictionary_file(self, first_letter: str) -> Dict:
    """Load dictionary file based on first letter of the word."""
    filename = f"D{first_letter.upper()}.json"
    try:
      with open(self.data_folder / filename) as f:
        return json.load(f)
    except FileNotFoundError:
      raise FileNotFoundError(f"Dictionary file for letter '{first_letter}' not found.")
    except json.JSONDecodeError:
      raise ValueError(f"Invalid JSON format in dictionary file for letter '{first_letter}'.")
  

class DictionaryFormatter:
  @staticmethod
  def format_nested_list(items: Union[List, str], indent: int = 1) -> List[str]:
    """Format nested lists into formatted strings with proper indentation."""
    formatted = []
    indent_str = '\t' * indent

    if isinstance(items, list):
      for item in items:
        formatted.extend(DictionaryFormatter.format_nested_list(item, indent))
    else:
      formatted.append(f"{indent_str}{items}")

    return formatted
  
  @staticmethod
  def format_meanings(meanings: Dict[str, List]) -> List[str]:
    """Format meanings dictionary into presentable strings."""
    if not meanings:
      return ["No meanings found."]
    
    formatted = []
    for pos, definitions in meanings.items():
      formatted.append(f"\t{pos}:")
      formatted.extend(DictionaryFormatter.format_nested_list(definitions, 2))
    return formatted


class EnglishDictionary:
  def __init__(self, data_folder: str = "data/"):
    self.loader = DictionaryLoader(data_folder)
    self.formatter = DictionaryFormatter()
    self.current_data: Dict = {}
    self.similarity_threshold = 0.7

  def lookup_word(self, word: str) -> Optional[DictionaryEntry]:
    """Look up a word in the dictionary."""
    # Load appropriate dictionary file if not already loaded
    first_letter = word[0]
    if not self.current_data or word[0].upper() not in self.current_data:
      self.current_data = self.loader.load_dictionary_file(first_letter)
    
    # Try different cases
    for word_case in [word.upper(), word.title(), word.lower()]:
      if word_case in self.current_data:
        entry_data = self.current_data[word_case]
        return DictionaryEntry(
          word=word_case,
          meanings=entry_data['MEANINGS'],
          antonyms=entry_data['ANTONYMS'],
          synonyms=entry_data['SYNONYMS']
        )
    return None
  
  def display_entry(self, entry: DictionaryEntry):
    """Display dictionary entry in a formatted way."""
    print(f"\nWord: {entry.word}")

    print("\nMEANINGS:")
    for line in self.formatter.format_meanings(entry.meanings):
      print(line)

    print("\nANTONYMS:")
    if entry.antonyms:
      for line in self.formatter.format_nested_list(entry.antonyms):
        print(line)
    else:
      print("No antonyms found.")

    print("\nSYNONYMS")
    if entry.synonyms:
      for line in self.formatter.format_nested_list(entry.synonyms):
        print(line)
    else:
      print("No synonyms found.")

  def find_similar_words(self, word: str) -> List[str]:
    """Find similar words using fuzzy matching."""
    return get_close_matches(word, list(self.current_data.keys()), n=3, cutoff=self.similarity_threshold)
  

def main():
  dictionary = EnglishDictionary()

  while True:
    word = input("\nEnter word to search definition (or '1' to quit): ").strip()

    if word == '1':
      break

    try:
      entry = dictionary.lookup_word(word)

      if entry:
        dictionary.display_entry(entry)
      else:
        similar_words = dictionary.find_similar_words(word)
        if similar_words:
          print(f"\nNo definition found for '{word}'. Did you mean '{similar_words[0]}'?")
          if input("Press 'y' for yes or any other keys for no: ").lower() == 'y':
            entry = dictionary.lookup_word(similar_words[0])
            if entry:
              dictionary.display_entry(entry)
        else:
          print(f"\nNo definition found for '{word}' and no similar words found.")

    except (FileNotFoundError, ValueError) as e:
      print(f"Error: {e}")
    #   print(f"\nNo definition found for '{word}' and no similar words found.")

if __name__ == "__main__":
  main()