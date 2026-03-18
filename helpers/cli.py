import argparse
from datetime import datetime
import sys
from time import sleep

class CliFormatter:

	SUPPORTED_COLORS = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
	}

	@classmethod
	def list_colors(cls, search:str) -> None:
		for color in cls.SUPPORTED_COLORS.keys():
			if search in color:
				print(color)


	@classmethod
	def validate_colors(cls, color):
		if color not in cls.SUPPORTED_COLORS.keys():
			raise ValueError(f"Unsupported color: {color}")

	@classmethod
	def color_text(cls, text: str, color: str) -> str:
		return f"\033[{cls.SUPPORTED_COLORS[color]}m{text}\033[0m"

	@classmethod
	def receive_input(cls):
		try:
			user_message = input("> ")
			cls.clear_input_line()
			return user_message

		except KeyboardInterrupt as e:
			cls.clear_input_line()
			return "exit"

	@staticmethod
	def sleepif(condition: bool, duraiton:float):
		if condition:
			sleep(duraiton)

	@staticmethod
	def clear_input_line():
		sys.stdout.write("\r\033[2K")
		sys.stdout.flush()

class LLMChatParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="llmchat",
            description="arguments for cmd-based chatbot"
        )
        self._add_session()
        self._add_appearance()
        self._add_roles()
        self._add_discovery()
        self._add_meta()

    def parse(self) -> argparse.Namespace:
        return self.parser.parse_args()

    def _add_session(self):
        group = self.parser.add_argument_group("session")
        group.add_argument("-m", "--model",
            type=str,
            # default="llama3.1:latest",
            default="granite3.1-moe:1b",
            help="model to use (default: llama3.1:latest)"
        )
        group.add_argument("-n", "--name",
            type=str,
            default=datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            help="chat session name (default: current timestamp)"
        )
        group.add_argument("-sys", "--system",
            type=str,
            default="You are a concise assistant",
            help="system prompt for the model (default: \"You are a concise assistant\")"
        )
        group.add_argument("-qr", "--quick-response",
            action="store_true",
            help="skip output delay used for visual effects"
        )

    def _add_appearance(self):
        group = self.parser.add_argument_group("appearance")
        group.add_argument("-c", "--color",
            type=str,
            default="green",
            help="output color (default: green) — see --list-colors"
        )

    def _add_roles(self):
        group = self.parser.add_argument_group("roles")
        group.add_argument("-r", "--role",
            type=str,
            default="helpful-assistant",
            help="select a role (default: helpful-assistant)"
        )
        group.add_argument("-rd", "--role-desc",
            type=str,
            help="role description — used with --add-role or --update-role"
        )
        group.add_argument("-ar", "--add-role",
            action="store_true",
            help="add a new role (requires --role and --role-desc)"
        )
        group.add_argument("-ur", "--update-role",
            action="store_true",
            help="update an existing role (requires --role and --role-desc)"
        )
        group.add_argument("-dr", "--delete-role",
            action="store_true",
            help="delete a role from the store (requires --role)"
        )

    def _add_discovery(self):
        group = self.parser.add_argument_group("discovery")
        group.add_argument("-lm", "--list-models",
            action="store_true",
            help="list available models"
        )
        group.add_argument("-lr", "--list-roles",
            action="store_true",
            help="list saved roles"
        )
        group.add_argument("-lh", "--list-history",
            action="store_true",
            help="list saved chats"
        )
        group.add_argument("-lc", "--list-colors",
            action="store_true",
            help="list supported colors"
        )
        group.add_argument("-s", "--search",
            type=str,
            default="",
            help="search within any list"
        )

    def _add_meta(self):
        group = self.parser.add_argument_group("meta")
        group.add_argument("-v", "--verbose",
            action="store_true",
            help="enable verbose output"
        )
        group.add_argument("--version",
            action="version",
            version="%(prog)s 1.0.0"
        )