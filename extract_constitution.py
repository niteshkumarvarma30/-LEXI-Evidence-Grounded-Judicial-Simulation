import pdfplumber
import re
from embeddings import embed
from db import insert

PDF_PATH = "data/constitution.pdf"

def extract_articles(text):
    """
    Splits Constitution text into Articles using regex.
    """
    pattern = r"(Article\s+\d+[A-Z]?\s*–?.*?)\n"
    splits = re.split(pattern, text)

    articles = []
    for i in range(1, len(splits), 2):
        title = splits[i].strip()
        body = splits[i + 1].strip() if i + 1 < len(splits) else ""
        articles.append((title, body))

    return articles


def main():
    full_text = ""

    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    if not full_text.strip():
        raise RuntimeError("❌ No text extracted from Constitution PDF")

    articles = extract_articles(full_text)

    print(f"📘 Found {len(articles)} Articles")

    for title, body in articles:
        if len(body) < 50:
            continue  # skip noise

        insert("constitution_articles", {
            "article_title": title,
            "article_text": body,
            "embedding": embed(body)
        })

    print("✅ Constitution successfully loaded into database")


if __name__ == "__main__":
    main()
