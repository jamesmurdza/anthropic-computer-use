# Anthropic Computer Use with E2B

This repository allows you to spawn Ubuntu Linux systems in the cloud and automate them using AI agents. It uses [Anthropic Claude](https://www.anthropic.com/claude) for reasoning and [E2B Desktop](https://github.com/e2b-dev/desktop/) for the secure cloud sandboxes. It's based on [this computer use demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) by Anthropic.

> ⚠️ **Caution:** While this agent runs in a secure cloud Sandbox, you should avoid giving it access to sensitive data (such as account login information) and supervise it to prevent unwanted behavior. In some circumstances, Claude will follow commands found on webpages or contained in images, overriding user instructions and causing Claude to make mistakes.

## Quickstart

### Prerequisites

This project requires:

- Python 3.11
  - macOS: `brew install python@3.11`
- ImageMagick:
  - macOS: `brew install imagemagick`
- API keys for [Anthropic](https://console.anthropic.com/settings/keys) and [E2B](https://e2b.dev/dashboard?tab=keys).

### Running the agent

First, copy `example.env` to `.env`, and add your E2B API key to the new file.

To start the server, run the following command in the project directory:

`sh start.sh`

You can then then access the Streamlit interface in your browser at http://localhost:8501.

With the open Streamlit interface open, you can configure your Anthropic API key.

Finally, enter a prompt to start the agent.
