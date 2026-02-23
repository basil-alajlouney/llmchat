import json
from pathlib import Path
from typing import Any, Dict

def verbose_print_init(verbose):
  return lambda *values: print(*values) if verbose else None

def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Reads a single JSON file and returns its content as a dictionary.
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise ValueError(f"File does not exist: {file_path}")
    
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(data: Dict[str, Any], directory: str, filename: str) -> None:
    """
    Writes a dictionary to a JSON file inside the given directory.
    Creates the directory if it does not exist.
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    
    file_path = dir_path / filename
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

BASE_DIR = "~/.local/share/llmchat"