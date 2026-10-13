"""python -m src.ingest.run  (runs once; also used as Render build step)"""
from src.ingest.load import run as load
from src.ingest.chunk import chunk_all
from src.ingest.embed_store import embed_and_store

if __name__ == "__main__":
    embed_and_store(chunk_all(load()))
