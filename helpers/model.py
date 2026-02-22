import ollama

from helpers.utils import read_json_file, write_json_file

def list_models(search:str):
  for model in ollama.list().models:
    if search in model.model:
      print(model.model)

def validate_model(model):
  if model not in [model.model for model in ollama.list().models]:
      raise ValueError(f"Unsupported model: {model}")

def add_message(lst:list, message:str, role:str) -> None:
  # role in [system, assistant, user]
  lst.append({"role":role, "content":message})

def add_role(role_name:str, role_desc:str) -> None:
  roles = read_json_file("store/roles.json")

  if role_name in roles.keys():
    raise ValueError(f"role already exists: {role_name}")
  
  roles[role_name] = role_desc
  write_json_file(roles, "store", "roles.json")

def list_roles(search: str) -> None:
  roles = read_json_file("store/roles.json")

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

def update_role(role_name:str, role_desc:str) -> None:
  roles = read_json_file("store/roles.json")

  if role_name not in roles.keys():
    raise ValueError(f"role doesn't exists: {role_name}")
  
  roles[role_name] = role_desc
  write_json_file(roles, "store", "roles.json")

def delete_role(role_name:str) -> None:
  roles = read_json_file("store/roles.json")

  if role_name not in roles.keys():
    raise ValueError(f"role doesn't exists: {role_name}")
  
  del roles[role_name]
  write_json_file(roles, "store", "roles.json")