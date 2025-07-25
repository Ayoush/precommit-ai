# Gemini Pre-Commit Check

This project uses a pre-commit hook to analyze staged files with the Gemini AI model. It checks for potential bugs, typos, debug statements, and areas for improvement.

## Getting Started

### Prerequisites

- Python 3.6+
- Git

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up the pre-commit hook:**

    This project comes with a pre-commit hook that runs the Gemini AI check. To enable it, you need to make the script executable:

    ```bash
    chmod +x .git/hooks/pre-commit
    ```

4.  **Set your Gemini API Key:**

    The script requires a Gemini API key to be set as an environment variable.

    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```

    To make this permanent, add it to your shell's profile file (e.g., `~/.bashrc`, `~/.zshrc`).

## Usage

Once installed, the pre-commit hook will run automatically every time you run `git commit`. It will analyze the staged files and report any issues found by the Gemini model.

-   If the check passes, the commit will proceed.
-   If the check fails, the commit will be aborted, and you will see a list of issues to fix.

### Skipping the check

To skip the pre-commit check for a specific commit, use the `--no-verify` flag:

```bash
git commit -m "Your message" --no-verify
```

## Debugging

To see the full request and response from the Gemini API, set the `GEMINI_CHECK_DEBUG` environment variable to `true`:

```bash
export GEMINI_CHECK_DEBUG=true
```
