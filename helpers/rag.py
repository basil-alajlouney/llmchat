"""
1 - storing:
  * add document (file path / raw text)
  * remove document
  * list documents
  * storage backend (local: ChromaDB)

2 - chunking:
  * split document into chunks (size + overlap configurable)
  * attach source metadata to each chunk (filename, chunk index)

3 - embedding:
  * embed chunks via Ollama (e.g. nomic-embed-text)
  * store vectors + metadata in ChromaDB

4 - retrieving:
  * by similarity (top-k vector search)
  * by metadata filter (source file, date, tags)
  * by ID

5 - context injection:
  * format retrieved chunks
  * inject into prompt before sending to model
"""