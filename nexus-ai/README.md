# Nexus AI

A neobrutalist dark-mode AI chatbot built with Python and Streamlit. Streams answers from any model on [OpenRouter](https://openrouter.ai), keeps your chats in SQLite, and works on desktop and mobile.

## Screenshots
Add screenshots to `docs/` and link them here after your first run.

## Features
- Streaming responses with Markdown and code blocks, plus a copy button
- New, search, rename, and delete chats (delete asks for confirmation)
- Model picker (live OpenRouter list, or any custom model ID), temperature, max tokens, system prompt
- API key status and a connection test
- Chat history saved in SQLite and restored on reload
- Responsive layout: the sidebar collapses on mobile
- Friendly errors for missing/invalid key, rate limits, timeouts, network loss, and bad models

## Stack
Python 3.11+, Streamlit, OpenAI SDK (pointed at OpenRouter), SQLite, python-dotenv, pytest.

## Architecture
```
app.py                 entry point, session state, send flow
src/ai/                provider.py (interface) + openrouter_provider.py
src/database/          db.py (connection, schema) + conversations.py (queries)
src/components/        sidebar, chat, chat_input, settings, styles (CSS)
src/config/settings.py env/secrets + defaults
src/utils/             validators, helpers
tests/                 pytest suite (no API key or network needed)
```
**Provider abstraction:** `ChatProvider` is a one-method interface. `OpenAICompatibleProvider` works with any OpenAI-compatible endpoint, so adding Groq or OpenAI means a new base URL and key. **Storage:** all SQL lives in `src/database/`; swap those two files to move to PostgreSQL.

## Install
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

## API key
Create an OpenRouter key at <https://openrouter.ai/keys>.
- **Local:** copy `.env.example` to `.env` and set `OPENROUTER_API_KEY`.
- **Streamlit Cloud:** app **Settings → Secrets**, add `OPENROUTER_API_KEY = "your_key"`.

Never commit `.env` or `.streamlit/secrets.toml` (both are in `.gitignore`).

## Run
```bash
streamlit run app.py
```

## Test
```bash
pytest
```

## Push to GitHub
```bash
git init && git add . && git commit -m "Nexus AI"
git branch -M main
git remote add origin https://github.com/<you>/nexus-ai.git
git push -u origin main
```

## Deploy on Streamlit Community Cloud
1. Create the GitHub repo and push (above).
2. Open <https://share.streamlit.io> and sign in.
3. Choose **Create app** and connect the repository.
4. Select the `main` branch.
5. Set the main file path to `app.py`.
6. Under **Advanced settings → Secrets**, add `OPENROUTER_API_KEY = "your_key"`.
7. Deploy, then open the live URL and send a message to verify.

## Known limitations
- **Cloud storage is not permanent.** Community Cloud's filesystem is ephemeral, so SQLite history can reset when the app restarts or redeploys. All visitors to one deployment also share the same database. Use a managed database (e.g. PostgreSQL) before relying on it.
- No login or per-user separation.
- Settings reset on page reload (chats persist).
- A failed reply is shown as an error and is not saved; resend the message to retry.
- Mobile layout is covered by responsive CSS but should be checked on your own devices.

## Future improvements
PostgreSQL backend, user accounts, saved settings, retry/regenerate button, file uploads, token/cost display.
