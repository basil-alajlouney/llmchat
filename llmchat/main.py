from datetime import datetime
import os

from dotenv import load_dotenv
from helpers.model import add_message, add_role, delete_role, init_default_role, list_models, list_roles, update_role, validate_model
from helpers.cli_formater import conversate, init_chat_dir, list_history, list_colors, init_messages, validate_colors

import argparse
import importlib.metadata

from helpers.utils import Config, read_json_file, verbose_print_init, write_json_file

def main():

  parser = argparse.ArgumentParser(
      prog="llmchat",
      description="arguments for cmd-based chatbot"
  )

  # ── Session ────────────────────────────────────────────────
  session = parser.add_argument_group("session")
  session.add_argument("-m", "--model",
      type=str,
      default="llama3.1:latest",
      help="model to use (default: llama3.1:latest)"
  )
  session.add_argument("-n", "--name",
      type=str,
      default=datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
      help="chat session name (default: current timestamp)"
  )
  session.add_argument("-sys", "--system",
      type=str,
      default="You are a concise assistant",
      help="system prompt for the model (default: \"You are a concise assistant\")"
  )
  session.add_argument("-qr", "--quick-response",
      action="store_true",
      help="skip output delay used for visual effects"
  )

  # ── Appearance ─────────────────────────────────────────────
  appearance = parser.add_argument_group("appearance")
  appearance.add_argument("-c", "--color",
      type=str,
      default="green",
      help="output color (default: green) — see --list-colors"
  )

  # ── Roles ──────────────────────────────────────────────────
  roles = parser.add_argument_group("roles")
  roles.add_argument("-r", "--role",
      type=str,
      default="helpful-assistant",
      help="select a roles (default: helpful-assistant)"
  )
  roles.add_argument("-rd", "--role-desc",
      type=str,
      help="role description — used with --add-role or --update-role"
  )
  roles.add_argument("-ar", "--add-role",
      action="store_true",
      help="add a new role (requires --role and --role-desc)"
  )
  roles.add_argument("-ur", "--update-role",
      action="store_true",
      help="update an existing role (requires --role and --role-desc)"
  )
  roles.add_argument("-dr", "--delete-role",
      action="store_true",
      help="delete a role from the store (requires --role)"
  )

  # ── Discovery ──────────────────────────────────────────────
  discovery = parser.add_argument_group("discovery")
  discovery.add_argument("-lm", "--list-models",
      action="store_true",
      help="list available models"
  )
  discovery.add_argument("-lr", "--list-roles",
      action="store_true",
      help="list saved roles"
  )
  discovery.add_argument("-lh", "--list-history",
      action="store_true",
      help="list saved chats"
  )
  discovery.add_argument("-lc", "--list-colors",
      action="store_true",
      help="list supported colors"
  )
  discovery.add_argument("-s", "--search",
      help="search within any list",
      default=""
  )

  # ── Meta ───────────────────────────────────────────────────
  meta = parser.add_argument_group("meta")
  meta.add_argument("-v", "--verbose",
      action="store_true",
      help="enable verbose output"
  )
  meta.add_argument("--version",
      action="version",
      version="%(prog)s 1.0.0"
  )

  args = parser.parse_args()
  verbose_print = verbose_print_init(args.verbose)

  # Session initilization
  load_dotenv()
  Config.BASE_DIR = os.environ.get("BASE_DIR", os.path.expanduser("~") + "/.local/share/llmchat")
  init_default_role()
  init_chat_dir()

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

  if args.list_history:
    list_history(args.search)
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

# Session Validation
  validate_colors(args.color)
  validate_model(args.model)

  # Preparing the chat
  post_response_fn = lambda : write_json_file(messages, os.path.join(Config.BASE_DIR, "store", "history"), args.name + ".json")
  messages = init_messages(args.name)
  system = args.system if args.system else read_json_file(os.path.join(Config.BASE_DIR, "store", "roles.json"))[args.role]

  # Updating role or Initilizing the chat
  if len(messages) == 0:
    add_message(messages, system, "system")
  else:
    system_messages = messages[0]["content"]
    args.role = next((k for k, v in read_json_file(os.path.join(Config.BASE_DIR, "store", "roles.json")).items() if v == system_messages), None)

  verbose_print("model:", args.model)
  verbose_print("role:", args.role)
  verbose_print("chat title:", args.name)
  conversate(messages, args.model, args.color, args.quick_response, post_response_fn)

if __name__ == "__main__":
  main()