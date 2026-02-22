import ollama


def validate_model(model):
  if model not in [model.model for model in ollama.list().models]:
      raise ValueError(f"Unsupported model: {model}")

def add_message(lst:list, message:str, role:str) -> None:
  # role in [system, assistant, user]
  lst.append({"role":role, "content":message})