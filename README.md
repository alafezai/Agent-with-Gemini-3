# Agent with Gemini

This project is a coding agent powered by Google's Gemini models.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables:**
    Make sure you have a `.env` file with your Gemini API key:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

## Usage

### Running the Basic Script

Currently, the main entry point is `main.py`. You can run it with a prompt:

```bash
python main.py "Your prompt here"
```

Example:
```bash
python main.py "Explain quantum computing"
```

## Project Structure

- `agent/`: Core agent logic (under development).
- `main.py`: Simple CLI interface for Gemini.
