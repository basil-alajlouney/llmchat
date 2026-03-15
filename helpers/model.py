import os
import ollama
from datetime import datetime

from helpers.cli import CliFormatter
from helpers.utils import Config, read_json_file, write_json_file

class Model:
	def __init__(self, model_name, conversation_title=None, system_prompt=None, role=None, history_dir=None, color="green", quick_response=False):
		self.history_dir = os.path.join(history_dir, conversation_title)
		self.history = read_json_file(self.history_dir) if os.path.exists(self.history_dir) else []
		self.model_name = model_name
		self.role = role
		self.system_prompt = system_prompt
		self.color = color
		self.quick_response = quick_response
		self.conversation_title = conversation_title if conversation_title is not None else \
							datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

		if len(self.history) == 0:
			self.add_message(self.system_prompt, "system")

	def add_message(self, message:str, role:str, store_message=False) -> None:
		assert role in ["system", "assistant", "user"], ValueError("Role doesn't exist")

		self.history.append({"role":role, "content":message})
		if store_message:
			write_json_file(self.history, self.history_dir)

	def chat(self, store_message=False):
		user_message = CliFormatter.receive_input()

		if user_message == "exit":
			return False

		self.add_message(user_message, "user", store_message)
		answer = ""
		role = None

		try:
			for chunk in ollama.chat(model=self.model_name, messages=self.history, stream=True):

				if not role:
					role = chunk.message.role

				for char in chunk.message.content:
					print(CliFormatter.color_text(char, self.color), end="", flush=True)
					answer += char
					CliFormatter.sleepif(not self.quick_response, 0.05)

					if char == " ":
						CliFormatter.sleepif(not self.quick_response, 0.08)
		except:
			pass

		print("")
		self.add_message(answer, "assistant", store_message)
		return True

	def conversate(self, store_messages=False):
		try:
			while self.chat(store_message=store_messages):...
			print("Ending chat...")
		except KeyboardInterrupt as e:
			print("\nEnding chat...")

	@staticmethod
	def list_models(search:str):
		for model in ollama.list().models:
			if search in model.model:
				print(model.model)

	@staticmethod
	def validate_model(model_name):
		if model_name not in [model.model for model in ollama.list().models]:
			raise ValueError(f"Unsupported model: {model_name}")

	@staticmethod
	def list_history(directory:str, search:str):
		for chat in os.listdir(directory):
			if search in chat[:-5]:
				print(chat[:-5])

class Roles:
    # the *_, **__ are used for compatability with invoking functions for cleaner code
	def __init__(self, roles_dir):
		self.roles = read_json_file(roles_dir)

	def __getitem__(self, role):
		return self.roles[role]

	@staticmethod
	def add_role(role_name:str, role_desc:str, directory, *_, **__) -> None:
		roles = read_json_file(directory)

		if role_name in roles.keys():
			raise ValueError(f"role already exists: {role_name}")

		roles[role_name] = role_desc
		write_json_file(roles, directory)
    
	@staticmethod
	def list_roles(directory, search:str="") -> None:
		roles = read_json_file(directory)

		for role, desc in roles.items():
			if search != "":
				print("Roles titles that match your search:")
		
		if search in role:
			print("=" * 20)
			print("Role title:", role)
			print("Description:", desc)

		if search != "":
			print("=" * 40, end="\n\n")
			print("Roles description that match your search:")

		if search in desc and search != "":
			print("=" * 20)
			print("Role title:", role)
			print("Description:", desc)

	@staticmethod
	def get_role_by_desc(directory:str, system_prompt:str):
		return next((k for k, v in read_json_file(directory).items() if v == system_prompt), None)

	@staticmethod
	def update_role(role_name:str, role_desc:str, directory) -> None:
		roles = read_json_file(directory)

		assert role_name not in roles.keys(), ValueError(f"role doesn't exists: {role_name}")

		roles[role_name] = role_desc
		write_json_file(roles, directory)

	@staticmethod
	def delete_role(role_name:str, *_, **__) -> None:
		roles = read_json_file(os.path.join(Config.BASE_DIR, "store", "roles.json"))

		assert role_name not in roles.keys(), ValueError(f"role doesn't exists: {role_name}")

		del roles[role_name]
		write_json_file(roles, Config.ROLES_DIR)

	@staticmethod
	def init_default_role():
		if not os.path.exists(os.path.join(Config.BASE_DIR, "store", "roles.json")):
			write_json_file({"helpful-assistant" : "you are a helpful assistant"}, Config.ROLES_DIR)