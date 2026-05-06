# Product Requirements Document — watchagonnawatch (CineBot)

## Vision
watchagonnawatch is a conversational AI assistant specialised exclusively in **movies and anime**. It helps users discover what to watch next, understand titles, plan watch orders, and get content-safety guidance — all through a fluid, mobile-first chat interface that feels as polished as a consumer streaming app.

---

## Target User
- Age 16–35, casual-to-enthusiast anime and film viewers
- Primarily on mobile; may open on tablet or desktop
- Wants confident, friendly recommendations without wading through review sites
- Ranges from "what should I watch tonight?" to "explain Evangelion's watch order"

---

## Must-Have Features

### 1. Topic-Specialised Chat
- Single `/chat` POST endpoint accepts a user message and returns a Gemini-generated response
- System instruction locks the bot to **movies + anime only**; off-topic questions receive a polite redirect
- Bot is **helpful by default**: general domain questions (genres, watch orders, spoiler-free reviews, content warnings, streaming availability guidance) are answered with appropriate disclaimers where relevant
- Bot refuses only: serious diagnoses/medical advice, prescription-level instructions, content that facilitates harm, or clearly off-topic requests (e.g., homework, politics)
- Responses rendered as formatted HTML via marked.js (Gemini outputs Markdown natively)

### 2. Image Upload with Topic Verification
- Image-upload button in the input bar sends image to `/vision` POST endpoint
- Gemini multimodal call analyses the image; if it is **not** movie/anime-related (e.g., homework, food photo, laptop error screen) the bot responds with a redirect message
- Accepted images: anime screenshots, movie stills, posters, streaming app title pages, Blu-ray covers, character references, manga panels (when purpose is anime identification), festival programme listings

### 3. Empty-Send Guard
- Send button is **disabled and visually dimmed** when the text input is empty or contains only whitespace
- Guard enforced at the frontend; cannot be bypassed by pressing Enter on a blank field

### 4. Markdown Rendering
- All bot responses parsed through marked.js (CDN) before insertion into the DOM
- Bold (`**`), italics (`*`), unordered lists, and inline code render as proper HTML — raw symbols never shown to the user

### 5. Rate-Limit & Error Handling
- HTTP 429: retry once after a 2-second back-off; if still failing, display friendly "I'm a bit busy right now — try again in a moment"
- HTTP 403 / PermissionDenied / GoogleAPIError: surface the **actual error message** in the chat bubble (e.g., "API key is invalid or has no permissions for this project") so students can debug bad keys immediately
- All other exceptions: logged server-side, user sees "Something went wrong — please retry"

### 6. UI — Existing Stitch Export (code.html)
- Use `code.html` as-is; do **not** redesign
- Remove all demo messages, placeholder text, and hardcoded sample conversation history
- Chat list starts empty; only real Gemini responses populate it
- Serve `code.html` at `/` from the FastAPI app on port 8000

---

## Non-Goals
- No user accounts, authentication, or persistent chat history across sessions
- No recommendation database or external movie API (TMDB, etc.) — all knowledge comes from Gemini
- No video playback or embedded trailers
- No support for topics outside movies and anime (video games, music, books, live sports)
- No piracy assistance or illegal streaming links
- No redesign of the existing UI

---

## Success Criteria
| Metric | Target |
|---|---|
| Empty-send guard | Send button disabled on blank/whitespace input — 100% of cases |
| Markdown rendering | `**bold**` and `*italic*` render as HTML in every bot bubble |
| Off-topic redirect | Bot politely declines and redirects for ≥ 95% of clearly off-topic inputs |
| Image topic guard | Non-movie/anime images trigger redirect message |
| 429 handling | Single retry + friendly message; never crashes |
| 403 handling | Actual error text shown in chat; never shows "busy" message for auth errors |
| Cold load time | Page interactive in < 2 s on a mid-range Android (4G) |
| Free-tier compliance | Stays within Gemini free tier: 15 RPM, 1 000 RPD, 1 M context |
