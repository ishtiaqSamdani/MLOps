## 📰 News Summarization Tool

A Streamlit app that:
- Extracts news content from a URL (Newspaper3k)
- Summarizes it with an LLM (LangChain `ChatOpenAI`)
- Classifies the article type (e.g., technology, financial)
- Saves summaries to a local JSON file
- Lets you ask questions over the saved summaries (Q&A)

### Features
- **URL extraction**: Title, text, publish date, authors
- **LLM summarization**: 3–4 sentence concise summary
- **Classification**: Single category label in lowercase
- **Storage**: Appends entries to `news_summaries.json`
- **Q&A**: Ask natural-language questions grounded in saved summaries

### Requirements
- Python 3.12+
- An OpenAI API key (`OPENAI_API_KEY`)
- Linux users: `python3.12-venv` (setup script installs it)

### Quick start
```bash
cd "/home/ishs/Desktop/Projects/MLops/MLOps/Gen-AI/5. Large Language Models/Kata"
bash setup.sh            # creates venv, installs deps, creates .env
# Edit .env and paste your OpenAI key
streamlit run app.py
```
Open `http://localhost:8501`.

### Manual setup
```bash
cd "/home/ishs/Desktop/Projects/MLops/MLOps/Gen-AI/5. Large Language Models/Kata"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp env.example .env     # then put OPENAI_API_KEY=...
streamlit run app.py
```

### Configuration
- `OPENAI_API_KEY`: required; read from `.env` or environment
- `OPENAI_MODEL` (optional): defaults to `gpt-3.5-turbo`
- Temperature is set in code to `0.3` for summarization and `0` for classification (via the same `llm` instance + tailored prompts)

### Usage
1. Paste a news article URL
2. Click "Summarize"
3. Review the summary card (date, type, title, summary)
4. The entry is appended to `news_summaries.json`
5. Use the "Ask Questions from Stored Summaries" section to query the saved summaries

### Data storage and schema
Summaries are saved in `news_summaries.json` (gitignored). Example entry:
```json
{
  "date": "2024-04-01",
  "summary": "... concise 3–4 sentence summary ...",
  "articleType": "technology",
  "title": "Some headline",
  "url": "https://example.com/article"
}
```

### How it works (high level)
- Extraction: Newspaper3k downloads and parses the article
- LLM: LangChain `LLMChain` with `ChatOpenAI` runs two prompts: summary and type classification
- UI: Streamlit; a session flag prevents repeated runs on rerender

### Troubleshooting
- Proxies/httpx error with OpenAI SDK: requirements pin `httpx<0.28` is included; ensure the venv uses these versions
- NLTK tokenizer error (rare with Newspaper3k):
  ```bash
  python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
  ```
- Extraction failures: some sites block scraping, or use heavy JS/paywalls; try another link
- API key errors: verify `.env` contains `OPENAI_API_KEY` or export it in the shell

### Development notes
- Core libs: Streamlit, LangChain (`langchain`, `langchain-openai`), Newspaper3k
- State: `st.session_state['do_summarize']` gates the summarize pipeline
- File layout:
  - `app.py` — UI and logic
  - `requirements.txt` — dependency pins
  - `setup.sh` — one-shot environment setup
  - `news_summaries.json` — local store (gitignored)

### Security and costs
- Keep your `OPENAI_API_KEY` private
- Prefer `gpt-3.5-turbo` to control costs; consider truncation/chunking for very long articles
- Use low temperature for classification to keep outputs deterministic


