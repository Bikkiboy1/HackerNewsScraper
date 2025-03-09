import requests
from bs4 import BeautifulSoup
import json


def fetch_html(url, pages=1):
    """
    Fetches the HTML content of the given URL for the specified number of pages.
    """
    html_pages = []

    for page in range(pages):
        page_url = f"{url}?p={page + 1}" if page > 0 else url
        response = requests.get(page_url)

        if response.status_code == 200:
            html_pages.append(response.text)
        else:
            print(f"\n⚠ Failed to fetch page {page + 1}. Status Code: {response.status_code}")

    return html_pages


def extract_headlines(html_pages):
    """
    Extracts headlines and their corresponding links from the given HTML pages.
    """
    headlines = []

    for html in html_pages:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".athing")

        for item in items:
            title_tag = item.select_one(".titleline a")
            if title_tag:
                title = title_tag.text
                link = title_tag["href"]
                headlines.append({"title": title, "link": link})

    return headlines


import json

def save_to_json(headlines, filename="headlines.json"):
    """
    Saves headlines to a JSON file while preventing duplicates.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
            # ✅ Ensure `existing_data` is always a list
            if not isinstance(existing_data, list):
                print("\n⚠ Invalid JSON format. Resetting data.")
                existing_data = []  # Reset to an empty list

    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_titles = {item["title"] for item in existing_data}  # Avoid duplicates
    new_data = [h for h in headlines if h["title"] not in existing_titles]

    if not new_data:
        print("\n⚠ No new headlines to add.")
        return

    existing_data.extend(new_data)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

    print(f"\n✅ {len(new_data)} new headlines added to {filename}!")
