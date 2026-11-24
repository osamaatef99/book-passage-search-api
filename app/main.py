from fastapi import FastAPI, Query

from .search import PassageIndex, load_passages

app = FastAPI(title="Book Passage Search", version="0.1.0")
index = PassageIndex(load_passages())


@app.get("/health")
def health():
    return {"status": "ok", "passages": len(index.passages)}


@app.get("/search")
def search(q: str = Query(..., min_length=2, max_length=200), top_k: int = Query(3, ge=1, le=10)):
    return {"query": q, "results": index.search(q, top_k=top_k)}
