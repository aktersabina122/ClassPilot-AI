# ClassPilot AI project prompt

## 1. ROLE

Act as a beginner-friendly Python web developer, chatbot designer, and prompt engineer. Build a small local student assignment and course information chatbot.

## 2. GOAL

Create a polished, easy-to-demo English chatbot named ClassPilot AI. It should help a student look up a sample course, assignment descriptions, due dates, and simple study suggestions.

## 3. CONTEXT

The project is for a class demonstration. Follow the same bounded chatbot pattern as a product FAQ assistant: a focused topic, separate local knowledge data, an Ollama model, and a web chat interface. Use fictional sample course data so the demo does not imply a real school's schedule. The student developer is new to coding and needs clear setup instructions.

## 4. TASK

Build a Python web app that loads course and assignment facts from a separate JSON file, finds a supported question, sends only approved facts to a local Ollama model, and returns a concise response. Provide a safe fixed response when a question is outside the supported topics or Ollama is unavailable.

## 5. REQUIREMENTS

- Use Python 3.13, Flask, and Ollama with `qwen3:0.6b` by default.
- Keep the course and assignment dataset separate from application code.
- Include at least 50 example phrasings for each supported question intent.
- Cover next due assignment, all assignments, assignment descriptions, course information, study planning, and how to use the chatbot.
- State the creator and owner as Sabina Akter when asked, using the identity record in the local dataset.
- Store conversation history and theme preference in the browser so refresh does not remove them.
- Include a polished responsive interface, theme switch, suggested questions, clear-chat control, sample course illustration, and README.
- The chat should work with an exact approved answer if Ollama is unavailable.

## 6. CONSTRAINTS

- Do not connect to a database, LMS, school account, cloud model, calendar, or external notification service.
- Do not invent assignment dates, course rules, instructor names, grades, or contact information.
- Do not claim to submit work or send reminders.
- Keep the chatbot within the sample AI-101 course and assignment-help topic.
- Treat the supplied dataset as demonstration data, not a real class schedule.

## 7. PROCESS

1. Load the local JSON knowledge file.
2. Match the question to a supported topic using example phrasings.
3. Select only the relevant approved course or assignment facts.
4. Ask the local Ollama model to write a short answer without adding facts.
5. Use a deterministic approved response if the model is unavailable.

## 8. OUTPUT

Provide the Python application, separate dataset, system prompt, web interface, dependency list, and beginner-friendly run guide. Package the complete runnable project in a ZIP archive.

## 9. QUALITY CHECK

Before delivery, check that the required files are present, JSON is valid, Python syntax parses, every intent has at least 50 example phrasings, answers do not exceed the supplied facts, and the README's model and startup instructions match the app configuration.
