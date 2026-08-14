import fitz  # PyMuPDF
import os
import re
import math
from collections import Counter


class BM25SearchEngine:
    """
    Lightweight, pure Python BM25 (Best Matching 25) search engine for text ranking.
    """
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.avg_doc_len = 0
        self.doc_lens = []
        self.doc_term_freqs = []
        self.idf = {}

        tokenized_corpus = [self._tokenize(doc) for doc in corpus]
        self.avg_doc_len = sum(len(doc) for doc in tokenized_corpus) / self.corpus_size if self.corpus_size > 0 else 0

        df = Counter()
        for doc in tokenized_corpus:
            self.doc_lens.append(len(doc))
            term_freq = Counter(doc)
            self.doc_term_freqs.append(term_freq)
            for term in term_freq:
                df[term] += 1

        for term, freq in df.items():
            # BM25 IDF formula with smoothing
            self.idf[term] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)

    def _tokenize(self, text):
        # Clean and split into alphanumeric tokens
        return re.findall(r'\b\w+\b', text.lower())

    def get_scores(self, query):
        query_terms = self._tokenize(query)
        scores = [0.0] * self.corpus_size

        for i in range(self.corpus_size):
            doc_len = self.doc_lens[i]
            term_freq = self.doc_term_freqs[i]
            score = 0.0

            for term in query_terms:
                if term in term_freq:
                    tf = term_freq[term]
                    idf_val = self.idf.get(term, 0.0)
                    # BM25 term weighting formula
                    numerator = idf_val * tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
                    score += numerator / denominator

            scores[i] = score

        return scores


class AcademicRAG:
    """
    Orchestrates page-level text extraction, indexing, and ranked retrieval.
    """
    def __init__(self):
        self.chunks = []  # Elements: {"text": str, "source": str, "page": int, "type": str}
        self.search_engine = None

    def add_pdf(self, file_path, doc_type):
        """
        Extract page text from PDF and index it with metadata.
        doc_type can be 'Syllabus', 'Textbook', 'Reference', 'Faculty Note'
        """
        if not file_path or not os.path.exists(file_path):
            return

        try:
            doc = fitz.open(file_path)
            filename = os.path.basename(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                if text and text.strip():
                    self.chunks.append({
                        "text": text.strip(),
                        "source": filename,
                        "page": page_num + 1,
                        "type": doc_type
                    })
            doc.close()
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")

    def build_index(self):
        """
        Index all accumulated chunks using BM25.
        """
        if not self.chunks:
            return
        corpus = [chunk["text"] for chunk in self.chunks]
        self.search_engine = BM25SearchEngine(corpus)

    def query(self, search_query, top_k=6):
        """
        Retrieve top K chunks matching the query, with priority boosts for notes and textbooks.
        """
        if not self.search_engine or not self.chunks:
            return []

        scores = self.search_engine.get_scores(search_query)
        boosted_scores = []

        # Apply source type priority boosts
        for i, score in enumerate(scores):
            chunk_type = self.chunks[i]["type"]
            boost = 1.0
            if chunk_type == "Faculty Note":
                boost = 1.6  # Highest priority
            elif chunk_type == "Textbook":
                boost = 1.3
            elif chunk_type == "Reference":
                boost = 1.1
            elif chunk_type == "Syllabus":
                boost = 0.8  # Syllabus is only fallback for topics

            boosted_scores.append((i, score * boost))

        # Sort descending by score
        boosted_scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in boosted_scores[:top_k]:
            results.append({
                "chunk": self.chunks[idx],
                "score": score
            })

        return results

    def get_combined_context(self, search_query, top_k=6):
        """
        Retrieve top K chunks and construct a single formatted context string.
        """
        results = self.query(search_query, top_k=top_k)
        if not results:
            return "No matching academic context found."

        context_parts = []
        for res in results:
            chunk = res["chunk"]
            header = f"[{chunk['type']} | Source: {chunk['source']} | Page {chunk['page']}]"
            context_parts.append(f"{header}\n{chunk['text']}")

        return "\n\n=========================================\n".join(context_parts)
