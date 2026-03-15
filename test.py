import pytest
from unittest.mock import patch
from helpers.cli import LLMChatParser
from llmchat.main import main

# ── Helpers ────────────────────────────────────────────────

def run(*args):
    """Run main() with given CLI args."""
    with patch("sys.argv", ["llmchat", *args]):
        main()

# ── Session ────────────────────────────────────────────────

class TestSession:

    def test_default_model(self):
        with patch("sys.argv", ["llmchat"]):
            from helpers.cli import LLMChatParser
            args = LLMChatParser().parse()
            assert args.model == "llama3.1:latest"

    def test_custom_model(self):
        with patch("sys.argv", ["llmchat", "-m", "llama3.2"]):
            args = LLMChatParser().parse()
            assert args.model == "llama3.2"

    def test_custom_model_long(self):
        with patch("sys.argv", ["llmchat", "--model", "llama3.2"]):
            args = LLMChatParser().parse()
            assert args.model == "llama3.2"

    def test_default_system_prompt(self):
        with patch("sys.argv", ["llmchat"]):
            args = LLMChatParser().parse()
            assert args.system == "You are a concise assistant"

    def test_custom_system_prompt(self):
        with patch("sys.argv", ["llmchat", "-sys", "You are a Python expert."]):
            args = LLMChatParser().parse()
            assert args.system == "You are a Python expert."

    def test_custom_name(self):
        with patch("sys.argv", ["llmchat", "-n", "my-session"]):
            args = LLMChatParser().parse()
            assert args.name == "my-session"

    def test_default_name_is_timestamp(self):
        with patch("sys.argv", ["llmchat"]):
            args = LLMChatParser().parse()
            import re
            assert re.match(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}", args.name)

    def test_quick_response_default_false(self):
        with patch("sys.argv", ["llmchat"]):
            args = LLMChatParser().parse()
            assert args.quick_response is False

    def test_quick_response_flag(self):
        with patch("sys.argv", ["llmchat", "-qr"]):
            args = LLMChatParser().parse()
            assert args.quick_response is True


# ── Appearance ─────────────────────────────────────────────

class TestAppearance:

    def test_default_color(self):
        with patch("sys.argv", ["llmchat"]):
            args = LLMChatParser().parse()
            assert args.color == "green"

    def test_custom_color(self):
        with patch("sys.argv", ["llmchat", "-c", "red"]):
            args = LLMChatParser().parse()
            assert args.color == "red"

    def test_custom_color_long(self):
        with patch("sys.argv", ["llmchat", "--color", "blue"]):
            args = LLMChatParser().parse()
            assert args.color == "blue"


# ── Roles ──────────────────────────────────────────────────

class TestRoles:

    def test_default_role(self):
        with patch("sys.argv", ["llmchat"]):
            args = LLMChatParser().parse()
            assert args.role == "helpful-assistant"

    def test_custom_role(self):
        with patch("sys.argv", ["llmchat", "-r", "devops"]):
            args = LLMChatParser().parse()
            assert args.role == "devops"

    def test_add_role_flag(self):
        with patch("sys.argv", ["llmchat", "-ar", "-r", "devops", "-rd", "You are a devops engineer."]):
            args = LLMChatParser().parse()
            assert args.add_role is True
            assert args.role == "devops"
            assert args.role_desc == "You are a devops engineer."

    def test_update_role_flag(self):
        with patch("sys.argv", ["llmchat", "-ur", "-r", "devops", "-rd", "Updated description."]):
            args = LLMChatParser().parse()
            assert args.update_role is True
            assert args.role == "devops"
            assert args.role_desc == "Updated description."

    def test_delete_role_flag(self):
        with patch("sys.argv", ["llmchat", "-dr", "-r", "devops"]):
            args = LLMChatParser().parse()
            assert args.delete_role is True
            assert args.role == "devops"

    def test_add_role_missing_desc(self):
        with patch("sys.argv", ["llmchat", "-ar", "-r", "devops"]):
            args = LLMChatParser().parse()
            assert args.role_desc is None   # validation should catch this in main()

    def test_role_desc_without_action(self):
        with patch("sys.argv", ["llmchat", "-rd", "some desc"]):
            args = LLMChatParser().parse()
            assert args.add_role is False
            assert args.update_role is False


# ── Discovery ──────────────────────────────────────────────

class TestDiscovery:

    def test_list_models(self):
        with patch("sys.argv", ["llmchat", "-lm"]):
            args = LLMChatParser().parse()
            assert args.list_models is True

    def test_list_roles(self):
        with patch("sys.argv", ["llmchat", "-lr"]):
            args = LLMChatParser().parse()
            assert args.list_roles is True

    def test_list_history(self):
        with patch("sys.argv", ["llmchat", "-lh"]):
            args = LLMChatParser().parse()
            assert args.list_history is True

    def test_list_colors(self):
        with patch("sys.argv", ["llmchat", "-lc"]):
            args = LLMChatParser().parse()
            assert args.list_colors is True

    def test_all_list_flags_default_false(self):
        with patch("sys.argv", ["llmchat"]):
            args = LLMChatParser().parse()
            assert args.list_models  is False
            assert args.list_roles   is False
            assert args.list_history is False
            assert args.list_colors  is False

    def test_search_default_empty(self):
        with patch("sys.argv", ["llmchat"]):
            args = LLMChatParser().parse()
            assert args.search == ""

    def test_search_with_value(self):
        with patch("sys.argv", ["llmchat", "-lm", "-s", "llama"]):
            args = LLMChatParser().parse()
            assert args.search == "llama"

    def test_search_long_flag(self):
        with patch("sys.argv", ["llmchat", "-lr", "--search", "dev"]):
            args = LLMChatParser().parse()
            assert args.search == "dev"


# ── Meta ───────────────────────────────────────────────────

class TestMeta:

    def test_verbose_default_false(self):
        with patch("sys.argv", ["llmchat"]):
            args = LLMChatParser().parse()
            assert args.verbose is False

    def test_verbose_flag(self):
        with patch("sys.argv", ["llmchat", "-v"]):
            args = LLMChatParser().parse()
            assert args.verbose is True

    def test_version_exits(self):
        with patch("sys.argv", ["llmchat", "--version"]):
            with pytest.raises(SystemExit) as e:
                LLMChatParser().parse()
            assert e.value.code == 0


# ── Combined ───────────────────────────────────────────────

class TestCombined:

    def test_model_and_color(self):
        with patch("sys.argv", ["llmchat", "-m", "llama3.2", "-c", "blue"]):
            args = LLMChatParser().parse()
            assert args.model == "llama3.2"
            assert args.color == "blue"

    def test_session_with_role(self):
        with patch("sys.argv", ["llmchat", "-m", "llama3.2", "-r", "devops", "-sys", "Be brief."]):
            args = LLMChatParser().parse()
            assert args.model  == "llama3.2"
            assert args.role   == "devops"
            assert args.system == "Be brief."

    def test_list_with_search(self):
        with patch("sys.argv", ["llmchat", "-lr", "-s", "dev"]):
            args = LLMChatParser().parse()
            assert args.list_roles is True
            assert args.search == "dev"