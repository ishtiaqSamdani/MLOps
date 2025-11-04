## Brief Report

### LLM integration for summarization
- We used LangChain’s `ChatOpenAI` as the LLM interface and built two `LLMChain`s with `PromptTemplate`s:
  - Summarization prompt: 3–4 sentence concise summary focusing on key points
  - Classification prompt: select exactly one category label (e.g., technology, financial)
- `get_llm()` is cached with `st.cache_resource` to avoid re-initializing the client on every rerun.
- The UI triggers the pipeline with a session flag to ensure a single run per click.

### Content extraction and processing
- Newspaper3k downloads and parses the article:
  - Extracted fields: `title`, `text`, `publish_date` (fallback to today), `authors`, `url`
- Processing pipeline per request:
  1) Extract article content
  2) Summarize via `LLMChain`
  3) Classify article type via a second `LLMChain`
  4) Render results in Streamlit and append to `news_summaries.json`
- Stored schema keys: `date`, `summary`, `articleType`, `title`, `url`
- A Q&A section answers questions grounded in the saved summaries using another `LLMChain` with a retrieval-like prompt over concatenated entries.

### Managing API usage costs
- Model choice: default `gpt-3.5-turbo` to balance quality and price
- Prompt discipline:
  - Clear, bounded summary instruction (3–4 sentences)
  - Deterministic classification (temperature 0 in the classification prompt context)
- State management: `st.cache_resource` prevents repeated client init; `st.session_state['do_summarize']` prevents accidental re-execution on reruns
- Potential further savings:
  - Chunking very long articles and doing map-reduce summaries
  - Truncating or summarizing the body before classification
  - Adding a vector store (e.g., FAISS/Chroma) for Q&A to avoid sending all summaries every time
  - Rate limiting/backoff to avoid retries and throttling penalties

### Challenges and lessons
- HTTP client/proxies incompatibility: An earlier version with direct OpenAI SDK hit a `proxies` argument issue tied to `httpx>=0.28`. Pinning `httpx<0.28` resolved it; later we standardized on LangChain’s `ChatOpenAI` path.
- Streamlit reruns: Clicking the button triggered repeated summarizations initially. Using `st.session_state['do_summarize']` and removing forced `st.rerun()` fixed duplicate runs.
- Extraction variability: Some publishers block scraping or return minimal text; surfaced errors gracefully and allow the user to try different URLs.
- Token limits: Extremely long articles can exceed model context. The current implementation passes the article text; for very long pages, chunking/truncation is recommended.

### Potential improvements
- Implement robust chunking + map/reduce summarization for long articles
- Maintain a vector store for Q&A to scale beyond a handful of summaries
- Add deduplication and metadata (source, author canonicalization)
- Configurable model/temperature in the UI; expose classification categories
- Better sidebar stats (filters by type/date range)
- Background jobs for extraction/summarization, with progress updates
- Automated tests for extraction and prompt stability
- Containerization (Docker) and deploy guides


