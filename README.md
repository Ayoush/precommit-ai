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

2.  **Set up a Python virtual environment:**

    It's recommended to use a virtual environment to manage project dependencies.

    ```bash
    python3 -m venv .venv
    ```

3.  **Activate the virtual environment:**

    -   **On macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    -   **On Windows (Command Prompt):**
        ```bash
        .venv\Scripts\activate.bat
        ```
    -   **On Windows (PowerShell):**
        ```bash
        .venv\Scripts\Activate.ps1
        ```

4.  **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Install pre-commit and set up the hooks:**

    This project uses `pre-commit` to manage and run its Git hooks.

    First, install `pre-commit` (it will be installed into your active virtual environment):

    ```bash
    pip install pre-commit
    ```

    Then, from the root of this repository, install the Git hooks:

    ```bash
    pre-commit install
    ```
    This command sets up the Git hooks in your local `.git/hooks` directory, pointing them to the `pre-commit` framework. The hooks will then run automatically on `git commit`.

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
