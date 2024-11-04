# Secure Computer Use by E2B

A secure cloud Linux computer powered by [E2B Desktop Sandbox](https://github.com/e2b-dev/desktop/) and controlled by Anthropic's Claude. Based on [the computer use demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo).

https://github.com/user-attachments/assets/07d42297-27f1-4119-8f4c-c102bf205b10

> ⚠️ **Caution:** While this agent runs in a secure cloud Sandbox, you should avoid giving it access to sensitive data (such as account login information) and supervise it to prevent unwanted behavior. In some circumstances, Claude will follow commands found on webpages or contained in images, overriding user instructions and causing Claude to make mistakes.

## Get started

### Prerequisites

- [git](https://git-scm.com/)
- [E2B API key](https://e2b.dev/dashboard?tab=keys)
- [Anthropic API key](https://console.anthropic.com/settings/keys)

### 1. Install the prerequisites

In your terminal:

```sh
brew install python@3.11 poetry imagemagick
```

### 2. Clone the repository

In your terminal:

```sh
git clone https://github.com/e2b-dev/secure-computer-use/
```

### 3. Set the environment variables

Enter the project directory:

```
cd secure-computer-use
```

Create a `.env` file in `secure-computer-use` and set the following:

```sh
# Get your API key here - https://e2b.dev/
E2B_API_KEY="your-e2b-api-key"
```

### 4. Start the web interface

Run the following command to start the web server:

```sh
sh start.sh
```

You can then now access the Streamlit interface in your browser at http://localhost:8501.

### 5. Configure the LLM

Finally, in the settings of the web app, configure the LLM provider you want to use.
