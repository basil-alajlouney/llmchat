from time import sleep
import ollama
import argparse
import sys
import importlib.metadata

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

def validate_colors(color):
    if color not in supported_colors.keys():
      raise ValueError(f"Unsupported color: {color}")

def validate_model(model):
  if model not in [model.model for model in ollama.list().models]:
      raise ValueError(f"Unsupported model: {model}")

def color_text(text: str, color: str) -> str:

  return f"\033[{supported_colors[color]}m{text}\033[0m"

def sleepif(condition: bool, duraiton:float):
  if condition:
    sleep(duraiton)

def add_message(lst:list, message:str, role:str) -> None:
  lst.append({"role":role, "content":message})

def clear_input_line():
    sys.stdout.write("\r\033[2K")
    sys.stdout.flush()

def main():

  parser = argparse.ArgumentParser(description="arguments for cmd-based chatbot")
  parser.add_argument("-m", "--model", type=str, default="llama3.1:latest", help="name the model you want to use, defualt: llama3.1:latest")
  parser.add_argument("-c", "--color", type=str, default="green", help="pick wish color you want to you, check --list-colors for supported colors, default: green")
  parser.add_argument("-s", "--system", type=str, default="You are a concise assistant.", help="system prompt for the model, default: You are a concise assistant")
  parser.add_argument("-qr", "--quick-response",action="store_true",default=False, help="discards sleep which is used to make responses more appealing")
  parser.add_argument("-v", "--version", action="store_true", defult=False, help="provide the version number")
  parser.add_argument("--list-models",action="store_true",default=False, help="list all available models")
  parser.add_argument("--list-colors",action="store_true",default=False, help="list all available colors")
  args = parser.parse_args()

  if args.list_colors:
    for color in supported_colors.keys():
      print(color)
    return

  if args.list_models:
    for model in ollama.list().models:
      print(model.model)
    return

  if args.version:
    print(importlib.metadata.version("llmchat"))
    return

  validate_colors(args.color)
  validate_model(args.model)

  messages = [
        {"role": "system", "content": args.system},
        # {"role": "user", "content": "Explain transformers in one word."}
        # {"role": "assistant", "content": "attention."}
    ]

  while True:

    try:
      user_message = input("> ")
      clear_input_line()

    except KeyboardInterrupt as e:
      clear_input_line()
      print("Ending chat...")
      return

    if user_message == "exit":
      print("Ending chat...")
      break

    add_message(messages, user_message, "user")
    answer = ""
    role = None

    for chunk in ollama.chat(model=args.model, messages=messages, stream=True):

      if not role:
        role = chunk.message.role

      for char in chunk.message.content:
        print(color_text(char, args.color), end="", flush=True)
        answer += char
        sleepif(not args.quick_response, 0.05)

        if char == " ":
          sleepif(not args.quick_response, 0.08)

    print("")
    add_message(messages, answer, "assistant")

if __name__ == "__main__":
  main()
