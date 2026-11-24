# Book Passage Search API (FastAPI + scikit-learn)

A small REST API that finds the passages most relevant to a question across a set of books. Based on the idea of the author's graduation project (an e-library with search inside books), reduced to a clean, tested service.

## Run
```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs, or: `GET /search?q=how many hours of sleep do adults need&top_k=3`

## Tests
`python -m pytest -q` (6 tests: relevance, ranking, no-match, validation, empty index, health)

## How it works
Each page is a passage. Passages are indexed with TF-IDF (unigrams + bigrams) and ranked by cosine similarity. Results below a minimum score are dropped, so unrelated questions return an empty list.

## Honest limits
This is lexical matching (word overlap), not true semantic search: "tired" will not match "sleepy". Next step is swapping the vectorizer for a sentence-embedding model. Sample books are dummy text.

## Project layout
`app/search.py` indexing and ranking, `app/main.py` API, `data/books.json` sample data, `tests/` pytest suite.
