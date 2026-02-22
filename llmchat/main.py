from helpers.model import add_message, validate_model
from helpers.cli_formater import conversate, validate_colors, clear_input_line, color_text, sleepif, supported_colors

import ollama
import argparse
import importlib.metadata

def main():

  # Parsers
  parser = argparse.ArgumentParser(description="arguments for cmd-based chatbot")
  subparsers = parser.add_subparsers(dest="command", required=False)

  # Model Parsers
  models_parser = subparsers.add_parser("list-models", help="list all available models")
  models_parser.add_argument("-s", "--search", type=str, default="")

  # Color Parsers
  colors_parser = subparsers.add_parser("list-colors", help="list all available colors")
  colors_parser.add_argument("-s", "--search", type=str, default="")

  # Chat Parsers
  parser.add_argument("-m", "--model", type=str, default="llama3.1:latest", help="name the model you want to use, defualt: llama3.1:latest")
  parser.add_argument("-c", "--color", type=str, default="green", help="pick wish color you want to you, check --list-colors for supported colors, default: green")
  parser.add_argument("-s", "--system", type=str, default="You are a helpfull assistant.", help="system prompt for the model, default: You are a concise assistant")
  parser.add_argument("-qr", "--quick-response",action="store_true",default=False, help="discards sleep which is used to make responses more appealing")
  parser.add_argument("-v", "--version", action="store_true", default=False, help="provide the version number")

  args = parser.parse_args()


  if args.command == "list-colors":
    for color in supported_colors.keys():
      if args.search in color:
        print(color)
    return

  if args.command == "list-models":
    for model in ollama.list().models:
      if args.search in model.model:
        print(model.model)
    return

  if args.version:
    print(importlib.metadata.version("llmchat"))
    return

  validate_colors(args.color)
  validate_model(args.model)

  messages = []
  add_message(messages, args.system, "system")

  conversate(messages, args.model, args.color, args.quick_response)

if __name__ == "__main__":
  main()