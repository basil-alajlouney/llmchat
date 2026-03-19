import os
import ollama
from datetime import datetime

from helpers.cli import CliFormatter
from helpers.utils import read_json_file, read_md_file, write_json_file, write_md_file

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

	def add_message(self, message:str, role:str, relevant_chunks=[], store_message=False) -> None:
		assert role in ["system", "assistant", "user"], ValueError("Role doesn't exist")

		data = {"role":role, "content":message, "relevant_chunks" : relevant_chunks}
		self.history.append(data)
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

	def get_role(role_name, directory):
		return os.path.join(directory, role_name)

	@staticmethod
	def add_role(role_name:str, role_desc:str, directory, *_, **__) -> None:
    
		if role_name.replace(" ", "_") in os.listdir(directory):
			raise ValueError(f"role already exists: {role_name}")

		file_dir = os.path.join(directory, role_name.replace(" ", "_"))

		write_md_file(file_dir, role_desc)
    
	@staticmethod
	def list_roles(directory, search:str="") -> None:
		search = search.replace(" ", "_")

		for role in os.listdir(directory):
			role_desc = read_md_file(os.path.join(directory, role))

			if search == "":
				print("All Roles Availble:")
			else:
				print("Roles titles that match your search:")

			if search in role or search in role_desc:
				print("Role title:", role)
				print("Description:", role_desc)
				print("=" * 20, end="\n")

	@staticmethod
	def get_role_by_desc(system_prompt:str, directory:str):
		for role in os.listdir(directory):
			role_desc = read_md_file(os.path.join(directory, role))

			if system_prompt == role_desc:
				return role

	@staticmethod
	def update_role(role_name:str, role_desc:str, directory) -> None:
		assert role_name.replace(" ", "_") in os.listdir(directory), ValueError(f"role doesn't exists: {role_name}")

		file_dir = os.path.join(directory, role_name.replace(" ", "_"))

		write_md_file(file_dir, role_desc)


	@staticmethod
	def delete_role(role_name:str, directory, *_, **__) -> None:
		assert role_name.replace(" ", "_") in os.lidtdir(directory), ValueError(f"role doesn't exists: {role_name}")
		os.remove(os.path.join(directory, role_name + ".md"))

	@staticmethod
	def init_default_role(directory):
		directory = os.path.join(directory, "helpful-assistant")
		base_role = """# System Prompt

You are a helpful and concise assistant.

- Provide clear, accurate, and relevant answers.
- Ask for clarification if the question is ambiguous.
- Keep responses focused and easy to understand."""
		if not os.path.exists(directory):
			write_md_file(base_role, directory)