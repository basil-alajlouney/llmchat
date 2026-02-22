from helpers.model import add_message, add_role, delete_role, list_models, list_roles, update_role, validate_model
from helpers.cli_formater import conversate, list_colors, validate_colors

import argparse
import importlib.metadata

from helpers.utils import read_json_file, verbose_print_init

def main():

  # Parsers
  parser = argparse.ArgumentParser(description="arguments for cmd-based chatbot")

  # Model Flags
  parser.add_argument("-m", "--model", type=str, default="llama3.1:latest", help="name the model you want to use, defualt: llama3.1:latest")
  
  # Format Flags
  parser.add_argument("-c", "--color", type=str, default="green", help="pick wish color you want to you, check --list-colors for supported colors, default: green")
  parser.add_argument("-sys", "--system", type=str, help="system prompt for the model, default: You are a concise assistant")
  parser.add_argument("-qr", "--quick-response", action="store_true",default=False, help="discards sleep which is used to make responses more appealing")
  
  # Roles Flags
  parser.add_argument("-ar", "--add-role", action="store_true",default=False, help="adds a new role to the store")
  parser.add_argument("-ur", "--update-role", action="store_true",default=False, help="updates a role in the store")
  parser.add_argument("-dr", "--delete-role", action="store_true",default=False, help="delete a role from the store")
  parser.add_argument("-r", "--role", default="helpful-assistant", help="delete a role from the store")
  parser.add_argument("-rd", "--role-desc", help="delete a role from the store")
  
  #Listing Flags
  parser.add_argument("-lc", "--list-colors", action="store_true",default=False, help="list all available colors")
  parser.add_argument("-lm", "--list-models", action="store_true",default=False, help="list all available models")
  parser.add_argument("-lr", "--list-roles", action="store_true",default=False, help="list all available roles")

  # Helper Flags
  parser.add_argument("-v", "--verbose", action="store_true", default=False, help="provide the version number")
  parser.add_argument("--version", action="store_true", default=False, help="provide the version number")
  parser.add_argument("-s", "--search", action="store_true", default="", help="search any given list")

  args = parser.parse_args()
  verbose_print = verbose_print_init(args.verbose)

  # Listing Conditionals
  if args.list_colors:
    list_colors(args.search)
    return

  if args.list_models:
    list_models(args.search)
    return

  if args.list_roles:
    list_roles(args.search)
    return

  # Roles Conditionals
  if args.add_role:
    add_role(args.role, args.role_desc)
    return

  if args.update_role:
    update_role(args.role, args.role_desc)
    return

  if args.delete_role:
    delete_role(args.role)
    return

  if args.version:
    print(importlib.metadata.version("llmchat"))
    return

  validate_colors(args.color)
  validate_model(args.model)

  messages = []
  system = args.system if args.system else read_json_file("store/roles.json")[args.role]
  add_message(messages, system, "system")

  verbose_print("model:", args.model, "\nrole:", args.role)
  conversate(messages, args.model, args.color, args.quick_response)

if __name__ == "__main__":
  main()