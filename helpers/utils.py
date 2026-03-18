import json
import os
from pathlib import Path
import sys
from typing import Any, Dict

def verbose_print_init(verbose):
    return lambda *values: print(*values) if verbose else None

def read_json_file(directory: str) -> Dict[str, Any]:
    """
    Reads a single JSON file and returns its content as a dictionary.
    """
    if not directory.endswith(".json"):
        directory += ".json"
    if not os.path.exists(directory):
        raise ValueError(f"File does not exist: {directory}")
    
    with open(directory, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(data: Dict[str, Any], directory: str) -> None:
    """
    Writes a dictionary to a JSON file inside the given directory.
    Creates the directory if it does not exist.
    """
    if not directory.endswith(".json"):
        directory += ".json"

    with open(directory, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def write_md_file(data:str, directory: str) -> None:
    """
    Writes a input into a md file inside the given directory.
    Creates the directory if it does not exist.
    """
    if not directory.endswith(".md"):
        directory += ".md"

    with open(directory, "w", encoding="utf-8") as f:
        f.write(data)

import os

def read_md_file(filename: str) -> str:
    """
    Reads a Markdown (.md) file using os and open, returns content as a string.
    
    Args:
        filename (str): Path to the Markdown file.
    
    Returns:
        str: File content.
    
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Markdown file '{filename}' not found")

    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def invoke_fn_by_dict(instance:Any, functions, args:tuple|list|dict|Any=(), kwargs:dict={}, exit=False):
    """invokes functions based on their presenese in instance

    Args:
        instance (Any): any instance with attributes
        functions (List): a list of the functions that will be matched
        args (tuple | list | dict | Any, optional): argumetns to be passed to the function invoked. Defaults to ().
        exit (Bool) : exits the program after completion in case a function was invoked
    """
    inovked = False
    for function_name, function in zip([f.__name__ for f in functions], functions):
        if getattr(instance, function_name):
            inovked = True
            function(*args, **kwargs)
    
    if exit and inovked:
        sys.exit()

class ClassLevelIndexingMeta(type):
    """In order to utilize this class an implementation of the function _getitem is required
    """
    def __getitem__(cls, *args, **kwargs):
        assert hasattr(cls, "_getitem"), AttributeError("Method _getitem not implemented")
        return cls._getitem(*args, **kwargs)
class Config:
    BASE_DIR = ""
    STORE_DIR = ""
    ROLES_DIR = ""
    HISTORY_DIR = ""

    @classmethod
    def setup(cls, base_dir: str):
        cls.BASE_DIR   = base_dir
        cls.STORE_DIR  = os.path.join(base_dir, "store")
        cls.ROLES_DIR  = os.path.join(cls.STORE_DIR, "roles")
        cls.HISTORY_DIR = os.path.join(cls.STORE_DIR, "history")

        os.makedirs(cls.BASE_DIR, exist_ok=True)
        os.makedirs(cls.STORE_DIR, exist_ok=True)
        os.makedirs(cls.ROLES_DIR, exist_ok=True)
        os.makedirs(cls.HISTORY_DIR, exist_ok=True)