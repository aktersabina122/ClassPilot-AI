# ClassPilot AI

ClassPilot AI is a small English-language chatbot created and owned by Sabina Akter. It answers questions about a fictional sample class, the AI-101 course, assignment descriptions, the next due assignment, and simple study planning. The course data is in a separate JSON file. Python and Flask serve the chat website, and Ollama with `qwen3:0.6b` provides locally generated wording.

This is a classroom demo. It is not connected to a real school, LMS, calendar, or notification service. Update the sample assignment data before presenting it as a real schedule.

## What is included

- `app.py` — Flask web app and chat endpoint
- `data/classpilot_knowledge.json` — editable sample course and assignment data, with 50 or more example phrasings per topic
- `prompts/system_prompt.txt` — answer scope and factuality rules
- `PROJECT_PROMPT.md` — the project idea arranged using the class prompt template
- `templates/` and `static/` — responsive chat interface, light/dark theme, and local illustration

## Requirements

- Python 3.13
- Ollama for AI-generated phrasing
- Windows, macOS, or Linux

If Ollama is unavailable, the app still answers recognized questions using approved data and a built-in deterministic response. Unrecognized or unrelated questions get a fixed scope response.

## Start on Windows (easy option)

1. Install Python 3.13 and Ollama.
2. Extract the ZIP archive.
3. Open the extracted `classpilot-ai` folder and double-click `START_WINDOWS.bat`.
4. On the first run, wait while it prepares the Python environment and installs packages. If asked whether to download `qwen3:0.6b`, type `Y` and press Enter to use Ollama. The download is about 523 MB. If you choose `N`, the built-in sample answers still work.
5. Keep the launcher window open. The chatbot opens at **http://127.0.0.1:5000**. Close the window or press `Ctrl+C` to stop it.

The launcher needs Python 3.13. If Python is missing, install it from python.org and enable **Add python.exe to PATH**, then double-click the launcher again.

## Start on Windows (manual option)

1. Install Python 3.13 and Ollama.
2. Open PowerShell in the extracted `classpilot-ai` folder.
3. Create and activate a virtual environment:

   ```powershell
   py -3.13 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the Python packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. In a separate terminal, download the small local model once:

   ```powershell
   ollama pull qwen3:0.6b
   ```

   Leave the Ollama app running. To use another installed model, set `OLLAMA_MODEL` to that model's name before starting Flask.

6. Start the website:

   ```powershell
   python app.py
   ```

7. Open **http://127.0.0.1:5000** in a browser.

## Start on macOS or Linux

From the extracted `classpilot-ai` directory:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
ollama pull qwen3:0.6b
python app.py
```

Then visit **http://127.0.0.1:5000**.

## Try these demo questions

- What is due next?
- Show all assignments.
- What is the prompt framework worksheet?
- What is this course about?
- Help me plan this week.
- Can you submit my assignment? (The assistant should explain that it cannot.)

## Update the sample data

Open `data/classpilot_knowledge.json` in a text editor to change the course description, assignment titles, dates, and descriptions. Keep dates in `YYYY-MM-DD` format. The included dates are examples; check that they are still in the future on the day of your presentation. Restart the app after editing the file.

You can add more example question phrasings to each intent's `phrases` list. The answer must remain supported by the data and the matching topic.

## Chat privacy

The browser keeps the displayed chat and theme in its local storage. The Python app does not save chat history to a server-side database. Questions matched to an intent are sent to the Ollama server configured in `OLLAMA_URL`, which defaults to the same computer at `http://localhost:11434`.
