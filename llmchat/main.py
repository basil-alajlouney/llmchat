import os

from dotenv import load_dotenv
from helpers.model import Model, Roles
from helpers.cli import LLMChatParser, CliFormatter

from helpers.utils import Config, invoke_fn_by_dict

def main():
    arg_parser = LLMChatParser()
    args = arg_parser.parse()

    # Session initilization
    load_dotenv()
    Config.setup(os.environ.get("BASE_DIR", os.path.expanduser("~") + "/.local/share/llmchat"))
    Roles.init_default_role()


    # Listing Conditionals
    invoke_fn_by_dict(args, [
        CliFormatter.list_colors,
        Model.list_models
    ], args=(args.search,), exit=True)

    invoke_fn_by_dict(args, [
        Roles.list_roles
    ], args=(Config.ROLES_DIR, args.search), exit=True)

    invoke_fn_by_dict(args, [
        Model.list_history,
    ], args=(Config.HISTORY_DIR, args.search), exit=True)

    # Roles Conditionals
    invoke_fn_by_dict(args, [
        Roles.add_role,
        Roles.update_role,
    ], args=(args.role, args.role_desc, Config.ROLES_DIR))

    invoke_fn_by_dict(args, [
        Roles.add_role,
        Roles.update_role,
    ], args=(args.role, args.role_desc, Config.ROLES_DIR))

    invoke_fn_by_dict(args, [
        Roles.delete_role
    ], args=(args.role,))

    # Session Validation
    CliFormatter.validate_colors(args.color)
    Model.validate_model(args.model)

    # Preparing the chat
    system_prompt = args.system if args.system else Roles()[args.role]
    llm = Model(
        args.model,
        args.name,
        system_prompt,
        Roles.get_role_by_desc(Config.ROLES_DIR, system_prompt),
        Config.HISTORY_DIR,
        color=args.color,
        quick_response=args.quick_response
    )

    # Updating role or Initilizing the chat
    if args.verbose:
        print("model:", llm.model_name)
        print("role:", llm.role)
        print("chat title:", llm.conversation_title)

    llm.conversate(store_messages=True)

if __name__ == "__main__":
    main()