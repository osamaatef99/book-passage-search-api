"""Passage search over a small book collection (TF-IDF + cosine similarity)."""
import json
from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "books.json"


@dataclass
class Passage:
    book: str
    page: int
    text: str


class PassageIndex:
    def __init__(self, passages: list[Passage]):
        if not passages:
            raise ValueError("no passages to index")
        self.passages = passages
        self.vectorizer = TfidfVectorizer(
            lowercase=True, stop_words="english", ngram_range=(1, 2), sublinear_tf=True
        )
        self.matrix = self.vectorizer.fit_transform(p.text for p in passages)

    def search(self, query: str, top_k: int = 3, min_score: float = 0.05) -> list[dict]:
        query = query.strip()
        if not query:
            return []
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix)[0]
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        out = []
        for i in ranked[:top_k]:
            if scores[i] < min_score:
                break
            p = self.passages[i]
            out.append({"book": p.book, "page": p.page, "score": round(float(scores[i]), 3), "text": p.text})
        return out


def load_passages(path: Path = DATA_FILE) -> list[Passage]:
    books = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Passage(b["title"], pg["page"], pg["text"]) for b in books for pg in b["pages"]]
