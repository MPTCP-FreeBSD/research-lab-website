import requests
from scholarly import scholarly
from fuzzywuzzy import fuzz
import os
import time
import re

# --- Step 1: Read Authors List ---
authors_file_path = "authors_list.txt"

def normalize_name(name):
    return name.replace("Dr.", "").replace("Prof.", "").replace("Mr.", "").strip().lower()

with open(authors_file_path, "r") as file:
    known_authors = [normalize_name(line.strip()) for line in file.readlines()]

print(f"✅ Loaded authors: {known_authors}")

# --- Step 2: Base Directory ---
BASE_DIR = "content/publication"
os.makedirs(BASE_DIR, exist_ok=True)

# --- Step 3: Fetch CrossRef Metadata ---
def fetch_crossref_metadata(title, retries=3, delay=5):
    url = f"https://api.crossref.org/works?query.bibliographic={title}&rows=1"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                items = response.json().get('message', {}).get('items', [])
                if items:
                    item = items[0]
                    return {
                        "type": item.get("type", "unknown"),
                        "abstract": re.sub(r'<.*?>', '', item.get("abstract", "")).replace("\n", " ").strip(),
                        "doi": item.get("DOI", ""),
                        "publisher": item.get("publisher", ""),
                        "volume": item.get("volume", ""),
                        "issue": item.get("issue", ""),
                        "pages": item.get("page", ""),
                        "published": item.get("issued", {}).get("date-parts", [[2000]])[0][0]
                    }
            return None
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(delay)
    return None

# --- Step 4: Categorize Paper ---
def categorize_paper(crossref_type):
    types = {
        'journal-article': ("2", "Journal Article"),
        'proceedings-article': ("1", "Conference Paper"),
        'posted-content': ("3", "Preprint"),
        'book': ("4", "Book"),
        'book-chapter': ("5", "Book Chapter"),
        'report': ("7", "Report"),
        'thesis': ("6", "Thesis"),
        'other': ("8", "Other")
    }
    return types.get(crossref_type, ("3", "Preprint"))

# --- Utilities ---
def clean_file_name(title):
    return title.replace(" ", "_").replace("/", "_").replace(":", "_")[:50]

def author_matches(authors_raw, known_authors, threshold=70):
    authors_list = [normalize_name(author) for author in authors_raw.split(",")]
    return any(fuzz.partial_ratio(pub_author, known) >= threshold for pub_author in authors_list for known in known_authors)

# --- Step 5: Process Publications ---
processed_titles = set()

for author_name in known_authors:
    print(f"\n🔍 Searching for author: {author_name}")
    try:
        search_query = scholarly.search_author(author_name)
        author = scholarly.fill(next(search_query), sections=["publications"])
    except StopIteration:
        print(f"❌ Author '{author_name}' not found. Skipping...")
        continue

    author_folder = os.path.join(BASE_DIR, author_name.replace(" ", "_"))
    os.makedirs(author_folder, exist_ok=True)

    for pub in author['publications']:
        scholarly.fill(pub)
        title = pub.get('bib', {}).get('title', 'Untitled Paper')
        authors_raw = pub.get('bib', {}).get('author', 'Unknown Authors')
        publication = pub.get('bib', {}).get('venue', 'N/A')
        cited_by = pub.get('num_citations', 0)
        tags = pub.get('bib', {}).get('keywords', '').split(",")
        link = pub.get('pub_url', '')

        if not title or title in processed_titles or not author_matches(authors_raw, known_authors):
            continue

        crossref = fetch_crossref_metadata(title)
        if not crossref:
            year = pub.get('bib', {}).get('year', '2000')
            abstract = ""
            publisher = ""
        else:
            year = str(crossref.get("published", "2000"))
            abstract = crossref.get("abstract", "")
            publisher = crossref.get("publisher", "")

        try:
            year_int = int(year)
            formatted_date = f"{year_int}-01-01"
        except:
            formatted_date = "2000-01-01"

        pub_type_code, pub_type_label = categorize_paper(crossref.get("type", "other") if crossref else "other")

        safe_title = clean_file_name(title)
        folder_path = os.path.join(author_folder, safe_title)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "index.md")

        authors_list = [author.strip() for author in authors_raw.split(",")]
        authors_yaml = "\n  - " + "\n  - ".join(authors_list)

        paper_data = f"""---
title: "{title}"
authors:{authors_yaml}
year: "{year}"
date: "{formatted_date}"
publication_types: ["{pub_type_code}"]  # {pub_type_label}
publication_type_label: "{pub_type_label}"
publication: "{publication}"
publisher: "{publisher}"
abstract: "{abstract}"
cited_by: "{cited_by}"
tags:
  - {", ".join(f'"{tag.strip()}"' for tag in tags if tag.strip())}

url_pdf: "{link}"
url_code: ""
url_dataset: ""
url_poster: ""
url_project: ""
url_slides: ""
url_source: ""
image:
  caption: ""
  focal_point: ""
  preview_only: false
projects: []
slides: ""
---
"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(paper_data)

        processed_titles.add(title)
        print(f"📄 Saved: {file_path}")

print("\n📅 All publications have been processed and saved.")
