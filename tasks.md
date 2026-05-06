# Build Tasks — watchagonnawatch (CineBot)

Complete these tasks in order. Each task is small and independently verifiable.

---

**Task 1 — Scaffold the project folder**
Create the project directory with `main.py`, `requirements.txt`, `.env.example`, and `.gitignore` (ignoring `.env`). Copy `code.html` into the folder root.

**Task 2 — Install dependencies and configure the API key**
Add `fastapi`, `uvicorn[standard]`, `google-generativeai`, `python-dotenv`, and `python-multipart` to `requirements.txt`. Create `.env` with `GEMINI_API_KEY=your_key_here` and load it in `main.py` using `python-dotenv` before any Gemini calls.

**Task 3 — Create the FastAPI app shell and serve code.html**
In `main.py`, initialise the FastAPI app, configure `google.generativeai` with the loaded key, and add a `GET /` route that returns `code.html` as an `HTMLResponse`. Verify the page loads at `http://localhost:8000`.

**Task 4 — Write the system instruction constant**
Define a `SYSTEM_INSTRUCTION` string in `main.py` that instructs the model to act as a friendly movies-and-anime expert: answer all general domain questions (recommendations, watch order, content warnings, streaming guidance) with disclaimers only where genuinely needed; politely redirect off-topic requests; refuse piracy links and harmful content; be spoiler-free by default.

**Task 5 — Implement the `/chat` POST endpoint**
Accept `{ "message": string, "history": [...] }`, build a Gemini `GenerativeModel` with `gemini-2.5-flash-lite` and the system instruction, start a chat session with the provided history, send the message, and return `{ "reply": response_text }`.

**Task 6 — Implement error handling for `/chat` (429, 403, and generic)**
Wrap the Gemini call: on HTTP 429 sleep 2 seconds and retry once — if still failing return a friendly "busy, try again" reply; on HTTP 403 / `PermissionDenied` / `GoogleAPICallError` return the **actual error message** (e.g., "API key invalid or has no permissions") — never swallow this as a "busy" message; on all other exceptions log the traceback and return a generic retry message.

**Task 7 — Implement the `/vision` POST endpoint**
Accept a multipart upload (`file` field as image bytes, optional `message` text field). Read the image, base64-encode it, and pass it to a Gemini multimodal call with the system instruction, instructing the model to redirect if the image is not movie/anime-related. Apply the same error handling as Task 6.

**Task 8 — Remove all demo data from code.html**
Delete every hardcoded `<div>` message bubble from `<main>` in `code.html`, clear the `value="..."` attribute from the text `<input>`, and remove any other placeholder or sample conversation content. The chat list must be empty on first load.

**Task 9 — Add the empty-send guard to code.html**
In the frontend JS, add an `input` event listener on the text field that disables the Send button (and dims it visually) whenever `input.value.trim() === ''`, and re-enables it otherwise. Also block the Enter key from submitting when the button is disabled.

**Task 10 — Integrate marked.js for Markdown rendering**
Add `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>` to `code.html`. Create an `appendMessage(role, markdownText)` helper that sets `element.innerHTML = marked.parse(markdownText)` for bot bubbles, so `**bold**`, `*italic*`, and `- lists` render as formatted HTML instead of raw symbols.

**Task 11 — Wire the send button and Enter key to `/chat`**
In the frontend JS, implement `sendMessage()`: append the user bubble, push the turn to a `conversationHistory` array, POST to `/chat` with the message and history, await the reply, append the bot bubble via `appendMessage()`, and update `conversationHistory` with the model's reply.

**Task 12 — Wire the image-upload button to `/vision`**
Add a hidden `<input type="file" accept="image/*">` triggered by the attachment icon. On file selection, show a preview thumbnail in the input area, then POST the image (and any typed text) to `/vision` as `multipart/form-data`. Append the bot's reply using `appendMessage()`.

**Task 13 — Add a loading / typing indicator**
While awaiting any Gemini response, append a temporary bot bubble with a "typing…" or animated-dots indicator. Remove it and replace with the real reply (or error message) once the response arrives.

**Task 14 — End-to-end smoke test**
Start the server with `uvicorn main:app --reload --port 8000` and verify: (a) empty input keeps Send disabled; (b) a movie question returns a formatted Markdown reply; (c) uploading a non-anime image triggers the redirect message; (d) a bad API key shows the actual error text in chat; (e) no demo messages appear on load.
