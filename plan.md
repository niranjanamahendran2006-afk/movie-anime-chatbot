# Implementation Plan — watchagonnawatch (CineBot)

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.11+) |
| AI Model | `gemini-2.5-flash-lite` via `google-generativeai` Python SDK |
| API Key | `GEMINI_API_KEY` loaded from `.env` via `python-dotenv` |
| Frontend | Vanilla JS — `code.html` used as-is, no framework |
| Markdown | `marked.js` loaded from CDN inside `code.html` |
| Server | Uvicorn (bundled with FastAPI) on port 8000 |

---

## Project Layout

```
watchagonnawatch/
├── .env                  # GEMINI_API_KEY=your_key_here
├── .env.example          # committed; .env in .gitignore
├── requirements.txt
├── main.py               # FastAPI app — all backend logic
└── code.html             # Stitch export — served at /
```

---

## Components — Build Order

### 1. Environment & Dependencies
Set up the project folder, `.env`, and `requirements.txt`.

```
fastapi
uvicorn[standard]
google-generativeai
python-dotenv
python-multipart      # for image file uploads
```

### 2. FastAPI App Shell (`main.py`)
- Load `GEMINI_API_KEY` from `.env` using `python-dotenv`
- Initialise `google.generativeai` client with the key
- Mount `code.html` to be served at `GET /`
- Define the system instruction (movies + anime specialist, helpful not paranoid)

### 3. System Instruction
Defined as a string constant. Key rules:
- Answer all general movie/anime questions (recommendations, watch order, content warnings, streaming guidance) — add disclaimers only where genuinely needed
- Refuse: off-topic requests, piracy links, harmful content
- Default spoiler-free; offer spoiler details only when user asks
- Tone: friendly expert

### 4. `/chat` POST Endpoint
```
POST /chat
Body: { "message": "string", "history": [ {"role": "user"|"model", "parts": ["string"]} ] }
Response: { "reply": "markdown string" }
```
- Pass `history` to maintain conversational context within the session (frontend manages history array in JS)
- Handle 429 with one 2 s retry
- Handle 403 / `google.api_core.exceptions.PermissionDenied` / `GoogleAPIError` — return actual error text
- Handle all other exceptions — log + generic retry message

### 5. `/vision` POST Endpoint
```
POST /vision
Body: multipart/form-data — file (image), message (optional text prompt)
Response: { "reply": "markdown string" }
```
- Read image bytes, encode as base64, pass to Gemini multimodal call
- System instruction instructs Gemini to redirect if image is not movie/anime-related
- Same error handling as `/chat`

### 6. Frontend Wiring (`code.html` modifications)
Changes are surgical — layout and styles untouched:

| What | How |
|---|---|
| Remove demo messages | Delete all hardcoded `<div>` message blocks from `<main>` |
| Remove placeholder input value | Clear `value="..."` from the `<input>` |
| Add `marked.js` | `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>` |
| Empty-send guard | `input.addEventListener('input', toggleSend)` — disables send button when `input.value.trim() === ''`; also blocks Enter key on empty input |
| Send on Enter | `input.addEventListener('keydown', e => { if (e.key === 'Enter' && !sendBtn.disabled) sendMessage() })` |
| Image upload button | Wire the attachment icon to a hidden `<input type="file" accept="image/*">` |
| Chat history state | JS array `conversationHistory` updated after each turn; sent with every `/chat` call |
| Append messages | `appendMessage(role, markdownText)` helper — creates bubble div, sets `innerHTML = marked.parse(markdownText)` |
| Loading indicator | Show a "typing…" bubble while awaiting response; remove on reply |
| Error display | On API error, append bot bubble with error text |

### 7. Markdown Rendering Detail
```javascript
// Never use innerHTML with raw text — always parse first
function appendMessage(role, text) {
  const bubble = document.createElement('div');
  bubble.innerHTML = marked.parse(text);   // safe for Gemini output
  // apply role-specific classes then append to <main>
}
```
`marked.js` converts `**bold**`, `*italic*`, `- list items` to proper HTML automatically.

### 8. Error Handling — Backend Detail
```python
import time
import google.generativeai as genai
from google.api_core.exceptions import PermissionDenied, GoogleAPICallError

def call_gemini_with_retry(fn):
    try:
        return fn()
    except Exception as e:
        status = getattr(e, 'code', None) or getattr(getattr(e, 'response', None), 'status_code', None)
        if status == 429:
            time.sleep(2)
            try:
                return fn()
            except:
                return {"reply": "I'm a bit busy right now — please try again in a moment."}
        if isinstance(e, (PermissionDenied, GoogleAPICallError)) or status == 403:
            return {"reply": f"API error: {str(e)}"}
        # everything else
        import logging; logging.exception("Gemini call failed")
        return {"reply": "Something went wrong — please retry."}
```

### 9. Run Instructions
```bash
# Install dependencies
pip install -r requirements.txt

# Add your key
echo "GEMINI_API_KEY=your_key_here" > .env

# Start server
uvicorn main:app --reload --port 8000

# Open in browser
open http://localhost:8000
```

---

## Free-Tier Limits (Gemini 2.5 Flash Lite)
| Limit | Value |
|---|---|
| Requests per minute | 15 RPM |
| Requests per day | 1 000 RPD |
| Context window | 1 M tokens |
| Multimodal | ✅ Supported |

The 2-second retry on 429 is intentional to stay within RPM budget without hammering the API.
