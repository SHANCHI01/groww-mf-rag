"""python -m scripts.fetch_reviews -> data/pulse/reviews.csv (public Groww Play Store reviews, last 12 weeks)."""
from datetime import datetime, timedelta
import pandas as pd
from google_play_scraper import reviews, Sort
from src.config import DATA

cut, rows, tok = datetime.now() - timedelta(weeks=12), [], None
while True:
    b, tok = reviews("com.nextbillion.groww", lang="en", country="in", sort=Sort.NEWEST, count=200, continuation_token=tok)
    rows += b
    if not b or b[-1]["at"] < cut or len(rows) > 3000: break
df = pd.DataFrame(rows)[["at", "score", "content"]]; df.columns = ["date", "rating", "text"]
df = df[df["date"] >= cut]
(DATA / "pulse").mkdir(parents=True, exist_ok=True)
df.to_csv(DATA / "pulse" / "reviews.csv", index=False)
print(f"saved {len(df)} reviews")
