# LLMChat CLI

A simple command-line interface to chat with **Ollama** models, with support for roles, chat history, custom system prompts, and color output.

## Installation

```bash
pip install git+https://github.com/basil-alajlouney/llmchat
```

> Requires Python 3.10+ and a running [Ollama](https://ollama.com) instance.

## Quick Start

```bash
# Start a chat with defaults
llmchat

# Use a specific model with a custom system prompt
llmchat -m llama3.1 -sys "You are a senior Python engineer."

# Resume a previous chat session
llmchat -n my-session
```

## Usage

```
llmchat [options]
```

### Session

| Flag | Default | Description |
|---|---|---|
| `-m`, `--model` | `llama3.1:latest` | Model to use |
| `-n`, `--name` | current timestamp | Chat session name (used to resume history) |
| `-sys`, `--system` | `You are a concise assistant` | System prompt for the model |
| `-qr`, `--quick-response` | — | Skip output delay used for visual effects |

### Appearance

| Flag | Default | Description |
|---|---|---|
| `-c`, `--color` | `green` | Output text color — see `--list-colors` |

### Roles

| Flag | Description |
|---|---|
| `-r`, `--role` | Select a role from the store (default: `helpful-assistant`) |
| `-rd`, `--role-desc` | Role description — used with `--add-role` or `--update-role` |
| `-ar`, `--add-role` | Add a new role (requires `--role` and `--role-desc`) |
| `-ur`, `--update-role` | Update an existing role (requires `--role` and `--role-desc`) |
| `-dr`, `--delete-role` | Delete a role from the store (requires `--role`) |

### Discovery

| Flag | Description |
|---|---|
| `-lm`, `--list-models` | List available Ollama models |
| `-lr`, `--list-roles` | List saved roles |
| `-lh`, `--list-history` | List saved chat sessions |
| `-lc`, `--list-colors` | List supported output colors |
| `-s`, `--search` | Search within any list |

### Meta

| Flag | Description |
|---|---|
| `-v`, `--verbose` | Enable verbose output |
| `--version` | Show version number |

## Examples

```bash
# Add a role
llmchat -ar -r devops -rd "You are a senior DevOps engineer specializing in Kubernetes."

# Start a session using that role
llmchat -r devops -n k8s-help

# Resume the session later
llmchat -n k8s-help

# List all saved chats and search through them
llmchat -lh -s
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally
- [ollama-python](https://pypi.org/project/ollama/) library

## Contributing

Open issues or submit pull requests on [GitHub](https://github.com/basil-alajlouney/llmchat).

## License

MIT License