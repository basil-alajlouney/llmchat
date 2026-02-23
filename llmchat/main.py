from datetime import datetime
from helpers.model import add_message, add_role, delete_role, init_default_role, list_models, list_roles, update_role, validate_model
from helpers.cli_formater import conversate, init_chat_dir, list_chats, list_colors, init_messages, validate_colors

import argparse
import importlib.metadata

from helpers.utils import BASE_DIR, read_json_file, verbose_print_init, write_json_file

def main():

  # Parsers
  parser = argparse.ArgumentParser(description="arguments for cmd-based chatbot")

  # Model Flags
  parser.add_argument("-m", "--model", type=str, default="llama3.1:latest", help="name the model you want to use, defualt: llama3.1:latest")
  parser.add_argument("-n", "--name", type=str, default=datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), help="name of the chat in the records, default would me the time")
  
  # Format Flags
  parser.add_argument("-c", "--color", type=str, default="green", help="pick wish color you want to you, check --list-colors for supported colors, default: green")
  parser.add_argument("-sys", "--system", type=str, help="system prompt for the model, default: You are a concise assistant")
  parser.add_argument("-qr", "--quick-response", action=BASE_DIR + "/" + "store_true",default=False, help="discards sleep which is used to make responses more appealing")
  
  # Roles Flags
  parser.add_argument("-ar", "--add-role", action=BASE_DIR + "/" + "store_true",default=False, help="adds a new role to theBASE_DIR + "/" +  store")
  parser.add_argument("-ur", "--update-role", action=BASE_DIR + "/" + "store_true",default=False, help="updates a role in theBASE_DIR + "/" +  store")
  parser.add_argument("-dr", "--delete-role", action=BASE_DIR + "/" + "store_true",default=False, help="delete a role from theBASE_DIR + "/" +  store")
  parser.add_argument("-r", "--role", default="helpful-assistant", help="delete a role from theBASE_DIR + "/" +  store")
  parser.add_argument("-rd", "--role-desc", help="delete a role from theBASE_DIR + "/" +  store")
  
  #Listing Flags
  parser.add_argument("-lc", "--list-colors", action=BASE_DIR + "/" + "store_true",default=False, help="list all available colors")
  parser.add_argument("-lm", "--list-models", action=BASE_DIR + "/" + "store_true",default=False, help="list all available models")
  parser.add_argument("-lr", "--list-roles", action=BASE_DIR + "/" + "store_true",default=False, help="list all available roles")
  parser.add_argument("-lch", "--list-chats", action=BASE_DIR + "/" + "store_true",default=False, help="list all available roles")

  # Helper Flags
  parser.add_argument("-v", "--verbose", action=BASE_DIR + "/" + "store_true", default=False, help="provide the version number")
  parser.add_argument("--version", action=BASE_DIR + "/" + "store_true", default=False, help="provide the version number")
  parser.add_argument("-s", "--search", action=BASE_DIR + "/" + "store_true", default="", help="search any given list")

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

  if args.list_chats:
    list_chats(args.search)
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

  # Session initilization
  validate_colors(args.color)
  validate_model(args.model)
  init_default_role()
  init_chat_dir()

  # Preparing the chat
  post_response_fn = lambda : write_json_file(messages, BASE_DIR + "/" + "store/chats", args.name + ".json")
  messages = init_messages(args.name)
  system = args.system if args.system else read_json_file(BASE_DIR + "/" + "store/roles.json")[args.role]

  # Updating role or Initilizing the chat
  if len(messages) == 0:
    add_message(messages, system, "system")
  else:
    system_messages = messages[0]["content"]
    args.role = next((k for k, v in read_json_file(BASE_DIR + "/" + "store/roles.json").items() if v == system_messages), None)

  verbose_print("model:", args.model)
  verbose_print("role:", args.role)
  verbose_print("chat title:", args.name)
  conversate(messages, args.model, args.color, args.quick_response, post_response_fn)

if __name__ == "__main__":
  main()