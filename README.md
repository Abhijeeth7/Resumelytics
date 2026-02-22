# Resumelytics 🚀

AI-powered resume optimizer that:

- Parses job descriptions
- Extracts required skills
- Evaluates candidate eligibility
- Computes ATS match score
- Generates weighted ATS fit

## Tech Stack

- Python
- NLP (rule-based + extensible)
- Modular ATS engine
- Resume parser pipeline

## Status

🚧 Active learning project  
🎯 Built for real-world ATS simulation

## Roadmap

- [ ] Chrome extension
- [ ] Reflex UI
- [ ] LLM resume rewriting
- [ ] Semantic JD understanding

## Local API (Shared by Web + Extension)

Run the local scoring API:

```powershell
venv\Scripts\python.exe local_api.py
```

Health check:

```powershell
curl http://127.0.0.1:8787/health
```

## Reflex Website

Run the Reflex app:

```powershell
cd web
..\venv\Scripts\python.exe -m reflex run
```

## Chrome Extension (MV3)

1. Open `chrome://extensions`
2. Enable Developer Mode
3. Click `Load unpacked`
4. Select the `extension/` folder
5. Keep `local_api.py` running, then use extension popup on a JD tab
