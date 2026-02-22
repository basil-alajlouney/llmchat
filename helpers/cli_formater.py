import sys
from time import sleep

import ollama
from helpers.model import add_message


supported_colors = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
}

def list_colors(search:str) -> None:
  for color in supported_colors.keys():
    if search in color:
      print(color)

def validate_colors(color):
    if color not in supported_colors.keys():
      raise ValueError(f"Unsupported color: {color}")
def color_text(text: str, color: str) -> str:

  return f"\033[{supported_colors[color]}m{text}\033[0m"
def sleepif(condition: bool, duraiton:float):
  if condition:
    sleep(duraiton)
def clear_input_line():
    sys.stdout.write("\r\033[2K")
    sys.stdout.flush()
    

def receive_input():
    try:
      user_message = input("> ")
      clear_input_line()
      return user_message

    except KeyboardInterrupt as e:
      clear_input_line()
      return "exit"

def chat(messages, model, color, quick_response):
  user_message = receive_input()

  if user_message == "exit":
    return False

  add_message(messages, user_message, "user")
  answer = ""
  role = None

  for chunk in ollama.chat(model=model, messages=messages, stream=True):

    if not role:
      role = chunk.message.role

    for char in chunk.message.content:
      print(color_text(char, color), end="", flush=True)
      answer += char
      sleepif(not quick_response, 0.05)

      if char == " ":
        sleepif(not quick_response, 0.08)

  print("")
  add_message(messages, answer, "assistant")
  return True

def conversate(messages, model, color, quick_response):
  while chat(messages, model, color, quick_response):
    continue
  print("Ending chat...")