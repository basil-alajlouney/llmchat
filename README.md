# LLMChat CLI

A simple command-line interface (CLI) to chat with **Ollama** models, with customizable options for colors, model selection, and system prompts.

## Features

- Chat with Ollama LLMs directly from your terminal.  
- Customize text color for outputs.  
- Select different models available in Ollama.  
- Set custom system prompts for context-aware responses.  
- Lightweight and easy to install.

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/basil-alajlouney/llmchat
````

> Requires Python 3.10+ and pip.

## Usage

Run the CLI:

```bash
llmchat
```

Optional arguments:

```bash
llmchat -m llama3.1 -s "You are a helpful assistant." -c green -qs
```

* `-m` / `--model` : Choose the Ollama model (e.g., `llama3.1`).
* `-s` / `--system-prompt` : Provide a system prompt for context.
* `-c` / `--color` : Set the color of the output text (e.g., `red`, `green`, `blue`).

### Example

```bash
llmchat -m llama3.1 -s "You are a concise assistant." -c cyan
> Hello, how do transformers work?
[cyan]Transformers use self-attention to model relationships between tokens in a sequence.[/cyan]
```

## Requirements

* Python 3.10+
* [Ollama Python library](https://pypi.org/project/ollama/)
* Optional: `rich` and `colorama` for enhanced output

## Contributing

Open issues or submit pull requests to improve the CLI functionality.

## License

MIT License

```
This is fully self-contained — everything a user needs to know is in **one file**, no extra split sections.  

If you want, I can also **add a small “quick start” snippet at the top** so users can literally copy-paste and chat in 2 commands. Do you want me to do that?
```
